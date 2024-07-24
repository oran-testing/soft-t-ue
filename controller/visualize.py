from scapy.all import *
import pyx
from pyx import bbox
from PIL import Image, ImageTk
import tkinter as tk

def packet_to_canvas(input_packet, layer_shift=0, rebuild=1):
    # type: (int, int) -> pyx.canvas.canvas
    if PYX == 0:
        raise ImportError("PyX and its dependencies must be installed")
    canvas = pyx.canvas.canvas()
    if rebuild:
        _, t = input_packet.__class__(raw(input_packet)).build_ps()
    else:
        _, t = input_packet.build_ps()
    YTXTI = len(t)
    for _, l in t:
        YTXTI += len(l)
    YTXT = float(YTXTI)
    YDUMP = YTXT

    XSTART = 1
    XDSTART = 10
    y = 0.0
    yd = 0.0
    XMUL = 0.55
    YMUL = 0.4

    backcolor = colgen(0.6, 0.8, 1.0, trans=pyx.color.rgb)
    forecolor = colgen(0.2, 0.5, 0.8, trans=pyx.color.rgb)
#        backcolor=makecol(0.376, 0.729, 0.525, 1.0)

    def hexstr(x):
        # type: (bytes) -> str
        return " ".join("%02x" % orb(c) for c in x)

    def make_dump_txt(x, y, txt):
        # type: (int, float, bytes) -> pyx.text.text
        return pyx.text.text(
            XDSTART + x * XMUL,
            (YDUMP - y) * YMUL,
            r"\tt{%s}" % hexstr(txt),
            [pyx.text.size.Large]
        )

    def make_box(o):
        # type: (pyx.bbox.bbox) -> pyx.bbox.bbox
        return pyx.box.rect(
            o.left(), o.bottom(), o.width(), o.height(),
            relcenter=(0.5, 0.5)
        )

    def make_frame(lst):
        # type: (List[Any]) -> pyx.path.path
        if len(lst) == 1:
            b = lst[0].bbox()
            b.enlarge(pyx.unit.u_pt)
            return b.path()
        else:
            fb = lst[0].bbox()
            fb.enlarge(pyx.unit.u_pt)
            lb = lst[-1].bbox()
            lb.enlarge(pyx.unit.u_pt)
            if len(lst) == 2 and fb.left() > lb.right():
                return pyx.path.path(pyx.path.moveto(fb.right(), fb.top()),
                                        pyx.path.lineto(fb.left(), fb.top()),
                                        pyx.path.lineto(fb.left(), fb.bottom()),  # noqa: E501
                                        pyx.path.lineto(fb.right(), fb.bottom()),  # noqa: E501
                                        pyx.path.moveto(lb.left(), lb.top()),
                                        pyx.path.lineto(lb.right(), lb.top()),
                                        pyx.path.lineto(lb.right(), lb.bottom()),  # noqa: E501
                                        pyx.path.lineto(lb.left(), lb.bottom()))  # noqa: E501
            else:
                # XXX
                gb = lst[1].bbox()
                if gb != lb:
                    gb.enlarge(pyx.unit.u_pt)
                kb = lst[-2].bbox()
                if kb != gb and kb != lb:
                    kb.enlarge(pyx.unit.u_pt)
                return pyx.path.path(pyx.path.moveto(fb.left(), fb.top()),
                                        pyx.path.lineto(fb.right(), fb.top()),
                                        pyx.path.lineto(fb.right(), kb.bottom()),  # noqa: E501
                                        pyx.path.lineto(lb.right(), kb.bottom()),  # noqa: E501
                                        pyx.path.lineto(lb.right(), lb.bottom()),  # noqa: E501
                                        pyx.path.lineto(lb.left(), lb.bottom()),  # noqa: E501
                                        pyx.path.lineto(lb.left(), gb.top()),
                                        pyx.path.lineto(fb.left(), gb.top()),
                                        pyx.path.closepath(),)

    def make_dump(s,   # type: bytes
                    shift=0,  # type: int
                    y=0.,  # type: float
                    col=None,  # type: pyx.color.color
                    bkcol=None,  # type: pyx.color.color
                    large=16  # type: int
                    ):
        # type: (...) -> Tuple[pyx.canvas.canvas, pyx.bbox.bbox, int, float]  # noqa: E501
        c = pyx.canvas.canvas()
        tlist = []
        while s:
            dmp, s = s[:large - shift], s[large - shift:]
            txt = make_dump_txt(shift, y, dmp)
            tlist.append(txt)
            shift += len(dmp)
            if shift >= 16:
                shift = 0
                y += 1
        if col is None:
            col = pyx.color.rgb.red
        if bkcol is None:
            bkcol = pyx.color.rgb.white
        c.stroke(make_frame(tlist), [col, pyx.deco.filled([bkcol]), pyx.style.linewidth.Thick])  # noqa: E501
        for txt in tlist:
            c.insert(txt)
        return c, tlist[-1].bbox(), shift, y

    last_shift, last_y = 0, 0.0
    while t:
        bkcol = next(backcolor)
        proto, fields = t.pop()
        y += 0.5
        pt = pyx.text.text(
            XSTART,
            (YTXT - y) * YMUL,
            r"\font\cmssfont=cmss10\cmssfont{%s}" % tex_escape(
                str(proto.name)
            ),
            [pyx.text.size.Large]
        )
        y += 1
        ptbb = pt.bbox()
        ptbb.enlarge(pyx.unit.u_pt * 2)
        canvas.stroke(ptbb.path(), [pyx.color.rgb.black, pyx.deco.filled([bkcol])])  # noqa: E501
        canvas.insert(pt)
        for field, fval, fdump in fields:
            col = next(forecolor)
            ft = pyx.text.text(XSTART, (YTXT - y) * YMUL, r"\font\cmssfont=cmss10\cmssfont{%s}" % tex_escape(field.name))  # noqa: E501
            if isinstance(field, BitField):
                fsize = '%sb' % field.size
            else:
                fsize = '%sB' % len(fdump)
            if (hasattr(field, 'field') and
                    'LE' in field.field.__class__.__name__[:3] or
                    'LE' in field.__class__.__name__[:3]):
                fsize = r'$\scriptstyle\langle$' + fsize
            st = pyx.text.text(XSTART + 3.4, (YTXT - y) * YMUL, r"\font\cmbxfont=cmssbx10 scaled 600\cmbxfont{%s}" % fsize, [pyx.text.halign.boxright])  # noqa: E501
            if isinstance(fval, str):
                if len(fval) > 18:
                    fval = fval[:18] + "[...]"
            else:
                fval = ""
            vt = pyx.text.text(XSTART + 3.5, (YTXT - y) * YMUL, r"{%s}" % tex_escape(fval.encode('ascii', 'ignore').decode('ascii')))  # noqa: E501
            y += 1.0
            if fdump:
                dt, target, last_shift, last_y = make_dump(fdump, last_shift, last_y, col, bkcol)  # noqa: E501

                dtb = target
                vtb = vt.bbox()
                bxvt = make_box(vtb)
                bxdt = make_box(dtb)
                dtb.enlarge(pyx.unit.u_pt)
                try:
                    if yd < 0:
                        cnx = pyx.connector.curve(bxvt, bxdt, absangle1=0, absangle2=-90)  # noqa: E501
                    else:
                        cnx = pyx.connector.curve(bxvt, bxdt, absangle1=0, absangle2=90)  # noqa: E501
                except Exception:
                    pass
                else:
                    canvas.stroke(cnx, [pyx.style.linewidth.thin, pyx.deco.earrow.small, col])  # noqa: E501

                canvas.insert(dt)

            canvas.insert(ft)
            canvas.insert(st)
            canvas.insert(vt)
        last_y += layer_shift

    return canvas

def write_to_pdf(canvas, file_path):
    canvas.writePDFfile(file_path)

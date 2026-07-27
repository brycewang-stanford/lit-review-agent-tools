import sys, time, json
t0=time.time()
from marker.converters.pdf import PdfConverter
from marker.models import create_model_dict
from marker.output import text_from_rendered
imp=time.time()-t0
src, out = sys.argv[1], sys.argv[2]
t1=time.time()
# pdftext's multiprocess worker dies on macOS; force single-process extraction.
conv=PdfConverter(artifact_dict=create_model_dict(), config={"pdftext_workers": 1})
rendered=conv(src)
text,_,images=text_from_rendered(rendered)
dur=time.time()-t1
open(out,"w",encoding="utf-8").write(text)
print(json.dumps({"tool":"marker","import_s":round(imp,1),"convert_s":round(dur,1),
                  "tables":text.count("\n|"),"pictures":len(images or {})}))

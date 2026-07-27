import sys, time, json
t0=time.time()
from docling.document_converter import DocumentConverter
imp=time.time()-t0
src, out = sys.argv[1], sys.argv[2]
t1=time.time()
res=DocumentConverter().convert(src)
md=res.document.export_to_markdown()
dur=time.time()-t1
open(out,"w",encoding="utf-8").write(md)
print(json.dumps({"tool":"docling","import_s":round(imp,1),"convert_s":round(dur,1),
                  "tables":len(res.document.tables),"pictures":len(res.document.pictures)}))

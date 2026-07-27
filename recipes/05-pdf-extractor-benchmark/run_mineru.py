import sys, time, os, json
os.environ.setdefault("MINERU_DEVICE_MODE", "cpu")
from mineru.cli.common import do_parse, read_fn

def main():
    src, outdir = sys.argv[1], sys.argv[2]
    name = os.path.splitext(os.path.basename(src))[0]
    t = time.time()
    do_parse(output_dir=outdir, pdf_file_names=[name],
             pdf_bytes_list=[read_fn(src)], p_lang_list=["en"], backend="pipeline")
    print(json.dumps({"tool": "mineru", "convert_s": round(time.time() - t, 1)}))

if __name__ == "__main__":   # required: mineru uses multiprocessing spawn
    main()

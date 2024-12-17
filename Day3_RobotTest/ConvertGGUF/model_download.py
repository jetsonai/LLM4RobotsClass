import argparse
from huggingface_hub import snapshot_download

parser = argparse.ArgumentParser()
parser.add_argument("--repo_id", default="llama-3.2-Korean-Bllossom-3B",
                        help="repo_id")
parser.add_argument("--home_dir", default="Bllossom",
                        help="home_dir") 
    
args = parser.parse_args()

print("===args.repo_id:{}".format(args.repo_id))
print("===args.home_dir:{}".format(args.home_dir))

hf_repo_id = args.home_dir+"/"+args.repo_id      
server_home_dir = "/home/jetsonai/models/"+args.home_dir

print("hf_repo_id:{}".format(hf_repo_id))
print("server_local_dir:{}".format(server_home_dir))

snapshot_download(repo_id=hf_repo_id, local_dir=server_home_dir)

#snapshot_download(repo_id="Bllossom/llama-3.2-Korean-Bllossom-3B", local_dir="/home/jetsonai/models/Bllossom/")

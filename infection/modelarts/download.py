import sys
from modelarts.session import Session

def download(obs_path, local_path):
    session = Session()
    session.obs.download_dir(obs_path, local_path)

if __name__ == "__main__":
    # Download dataset from OBS to local
    download(sys.argv[1], sys.argv[2])

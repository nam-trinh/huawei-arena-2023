# [Huawei Tech Arena 2023](https://huawei.agorize.com/en/challenges/irchack2023/)
<p align="center"> <img width="800" alt="screen" src="imgs/huawei/banner.png"> </p>

## Competition Detail

<p align="center"> <img width="500" alt="screen" src="imgs/huawei/Infectious.drawio.png"> </p>

<p align="center"> <img width="500" alt="screen" src="imgs/huawei/InfectiousBPMN.svg"> </p>



## Setup
- Execute the following command:
```
cd huawei-arena-2023
pip install -e .
```

- Use the notebook: [infection-sql-UI.ipynb](./notebooks/infection-sql-UI.ipynb)

## Docker
- Build docker using
```
cd huawei-arena-2023
DOCKER_BUILDKIT=1 docker build -t huawei:latest .
```

- Run docker using
```
docker run -it -p 8008:8008 --gpus all huawei:latest
```

- Inside docker container, run notebook using
```
sh jupyter.sh
```

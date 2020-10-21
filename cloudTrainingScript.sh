#!/bin/bash
sudo yum install git -y
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O /home/ec2-user/miniconda.sh
cd /home/ec2-user
bash ./miniconda.sh -b -p /home/ec2-user/miniconda
git clone https://github.com/JustinGuese/reinforcement-learning-trading-bot
cd reinforcement-learning-trading-bot
/home/ec2-user/miniconda/bin/conda init bash
source /home/ec2-user/.bashrc
conda create --name trading -y
source activate trading
conda install pip -y 
# sometimes theres a memory error, use this instead
pip install --no-cache-dir tensorflow
pip install -r requirements.txt
sudo chown -R ec2-user:ec2-user .
# reqs


screen -S trainer
python train.py data/BTCUSD\=X_1d_all.csv data/BTCUSD\=X_1d_test.csv --model-name btcusd1d
git add -A
git commit -m "training done"
git push origin master
# this will need sudo
shutdown -h now

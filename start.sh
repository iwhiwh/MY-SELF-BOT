if [ -z $UPSTREAM_REPO ]
then
  echo "Cloning main Repository"
  git clone https://github.com/iwhiwh/MY-SELF-BOT /MY-SELF-BOT
else
  echo "Cloning Custom Repo from $UPSTREAM_REPO "
  git clone $UPSTREAM_REPO /MY-SELF-BOT
fi
cd /MY-SELF-BOT
pip3 install -U -r requirements.txt
echo "Starting....................."
python3 bot.py

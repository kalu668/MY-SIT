lsblk
aws ec2 describe-volumes --filters Name=attachment.instance-id,Values=$(curl -s http://169.254.169.254/latest/meta-data/instance-id) --query 'Volumes[*].[VolumeId,Size]' --output table
lsblk
curl -s http://169.254.169.254/latest/meta-data/instance-id
TOKEN=$(curl -s -X PUT "http://169.254.169.254/latest/api/token" -H "X-aws-ec2-metadata-token-ttl-seconds: 21600") && curl -s -H "X-aws-ec2-metadata-token: $TOKEN" http://169.254.169.254/latest/meta-data/instance-id
aws ec2 describe-volumes --filters Name=attachment.instance-id,Values=i-0e5a600684b25545f --query 'Volumes[*].[VolumeId,Size]' --output table
aws ec2 modify-volume --volume-id vol-08b960439184d9c07 --size 20
sudo growpart /dev/xvda 1
sudo resize2fs /dev/xvda1
df -h /
aws ec2 describe-volumes --query 'Volumes[*].[VolumeId,Size]' --output table
lsblk
aws ec2 attach-volume --volume-id vol-0e3fa2adae2eb8893 --instance-id i-0e5a600684b25545f --device /dev/xvdb
df -h /
lsblk
sudo mkdir -p /mnt/data
sudo mount /dev/xvdb1 /mnt/data
df -h
du -sh /mnt/data/* 2>/dev/null | sort -rh | head -20
ls -lah /mnt/data/home/ubuntu/
cp -r /mnt/data/home/ubuntu/* ~/
ls ~/
rm -rf ~/coach ~/projects ~/node_modules ~/package.json ~/package-lock.json ~/*.py ~/*.md ~/*.txt ~/*.tar.gz ~/*.html ~/*.png
ls ~/
aws ec2 modify-volume --volume-id vol-0e3fa2adae2eb8893 --size 20
sudo growpart /dev/xvdb 1
sudo resize2fs /dev/xvdb1
df -h /mnt/data
curl -fsSL https://ollama.com/install.sh | sh
ollama serve
ollama pull llama3.2
ollama run llama3.2
systemctl status ollama
sudo systemctl start ollama
sudo systemctl enable ollama
ollama run llama3.2
npm install -g @google/gemini-cli
gemini
curl -fsSL https://deb.nodesource.com/setup_22.x | sudo -E bash -
sudo apt install -y nodejs
node --version
npm --version
npm install -g @google/gemini-cli
sudo npm install -g @google/gemini-cli
gemini
gemini 
gemini
aws ec2 modify-volume --volume-id vol-XXXXXXXXXXXXXXXXX --size 20
sudo snap install aws-cli --classic
aws ec2 modify-volume --volume-id vol-XXXXXXXXXXXXXXXXX --size 20
aws login
aws configure
aws ec2 modify-volume --volume-id vol-XXXXXXXXXXXXXXXXX --size 20
aws ec2 describe-volumes --query 'Volumes[*].[VolumeId,Size]' --output table
gemini
cd /home/ubuntu/coach
git push origin master
git auth login
git login
gh auth login
git auth
exit
git add
gemini
git auth login
git login
git-cli login
gemini
geminni
gemini
curl -fsSL https://antigravity.google/cli/install.sh | bash
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
agy
gemini
sudo  npm install -g neon-cli
neon auth
neon
neon login
gemini
npx neonctl@latest init
gemini
npm install -g @google/gemini-cli@0.46.0
rm -rf venv
python3 -m venv venv
apt install python3.14-venv
gemini
copilot
sudo snap install copilot-cli
copilot
gemini
my site
gemini
exit
gemini
apt list --upgradable
apt upgrade all
sudo apt upgrade all
sudo apt upgrade -all
sudo apt update
sudo apt upgrade -y
npm update -g @google/generative-ai
gemini

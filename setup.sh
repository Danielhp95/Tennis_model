sudo apt install python-pytest
sudo apt install python-pip
pip install -r requirements.txt

cd src/omalley/
bash "swig_wrap.sh"
cd ../../

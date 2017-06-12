sudo apt install python-pytest
sudo apt install python-pip
pip install -r requirements.txt

# CURRENT VERSION DOES NOT CONTAIN O_MALLEY equations
cd src/omalley/
bash "swig_wrap.sh"
cd ../../

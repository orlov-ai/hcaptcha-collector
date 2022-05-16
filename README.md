# hcaptcha-collector
A Flask app to collect hcaptcha images.  
This repository is used to collect hcaptcha images for this repo: https://github.com/orlov-ai/hcaptcha-dataset

## How to use

1. Obtain sitekey and secretkey from hCaptcha website. Head to https://www.hcaptcha.com/ and sign up.
Set new site and add `test.mydomain.com` as website url. Save you sitekey and secretkey, it is necessary in the next steps.
Set the difficulty to 'Always On'.
2. Edit your /etc/hosts file. Add a line `127.0.0.1       test.mydomain.com`. 
It is necessary because hCaptcha doesn't support localhost as a domain. 
You need to use non-localhost domain. `test.mydomain.com` is hardcoded in the code in this repository. 
3. Install requirements. I suggest creating a new python environment. Python 3.6+ supported.  
```pip install -r requirements.txt```
4. Setup up environment variables  
`HCAPTCHA_DATASET_PATH` - make a clean directory where captcha images will be collected.  
`HCAPTCHA_SITEKEY` - your hCaptcha sitekey  
`HCAPTCHA_SECRETKEY` - your hCaptcha secretkey
5. In separate windows run `python app.py` first then `python collect_hcaptcha.py`
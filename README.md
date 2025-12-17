# TA-Solarwinds-api
-----------------------------------------------------------------------------------------
App For Communicationg with Solarwinds API
Knowledge of SWQL can help .. SWQL Studio can be obtained from here: https://github.com/solarwinds/OrionSDK/releases
Solarwinds SDK obtained from: https://github.com/solarwinds/OrionSDK

After Importing SDK to Splunk App python scripts would fail with error:
ImportError: urllib3 v2 only supports OpenSSL 1.1.1+, currently the 'ssl' module is compiled with 'OpenSSL 1.0.2zk-fips  3 Sep 2024'. See: https://github.com/urllib3/urllib3/issues/

Fix was to update version of urllib3:
pip install urllib3==1.26.18 --target /opt/splunk/etc/apps/TA-Solarwinds-api/bin --upgrade

storage/passwords can be populated with the following:
curl -k -u admin https://localhost:8089/servicesNS/nobody/TA-Solarwinds-api/storage/passwords -d name=admin -d password=<myPassword>

-----------------------------------------------------------------------------------------

-------
Scripts
-------



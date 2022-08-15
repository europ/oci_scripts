### Disable instance legacy IMDS endpoints

Disable legacy instance metadata service (IMDS) for each instance in a particular OCI compartment.

#### Abstract

* Disabling Requests to the Legacy IMDSv1 Endpoints
    * https://docs.oracle.com/en-us/iaas/Content/Compute/Tasks/gettingmetadata.htm#upgrading-v2__disable-legacy

#### Prerequisites

* Python 3
* Python 3 packages
    * defined in `requirements.txt` file
    * see [Dependencies](#dependencies) section
* correctly configured OCI CLI
    * see https://docs.oracle.com/en-us/iaas/Content/API/Concepts/sdkconfig.htm
    * by default, `$HOME/.oci/config` configuration file is used
        * by default `[DEFAULT]` profile is used

#### Dependencies

```bash
python3 -m pip install -r requirements.txt
```

#### Help

```bash
python3 disable_instance_legacy_IMDS_endpoints.py --help
```

#### Example

```bash
python3 disable_instance_legacy_IMDS_endpoints.py --compartment_id ocid1.compartment.oc1..aaaaaaaaaaaaaaaaaaa
```

### Remove orphaned block volumes

Remove all orphaned block volumes that are not attached to any instance in a particular OCI compartment.

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
python3 remove_orphaned_block_volumes.py --help
```

#### Example

```bash
python3 remove_orphaned_block_volumes.py --delete --compartment_id ocid1.compartment.oc1..aaaaaaaaaaaaaaaaaaa
```

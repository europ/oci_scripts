#!/usr/bin/env python3

import click
import oci
import logging

@click.command()
@click.option('-c', '--compartment_id',
  help='Compartment ID.',
  required=True,
  type=str,
)
@click.option('-f', '--config_file',
  help='OCI configuration file path.',
  required=False,
  type=str,
  default="~/.oci/config",
  show_default=True,
)
@click.option('-p', '--profile_name',
  help='OCI configuration profile name.',
  required=False,
  type=str,
  default="DEFAULT",
  show_default=True,
)
@click.help_option('-h', '--help')
def main(compartment_id, config_file, profile_name):
    logging.basicConfig(
        level = logging.DEBUG,
        format='%(asctime)-s | %(pathname)s:%(lineno)s | %(levelname)-s | %(message)s',
        datefmt='%d-%m-%Y %H:%M:%S'
    )
    logging.info("Successfully started.")

    # load local configuration ([DEFAULT] profile from $HOME/.oci/config file)
    logging.info("OCI configuration > loading.")
    oci_configuration = oci.config.from_file(file_location=config_file, profile_name=profile_name)
    logging.info("OCI configuration > successfully loaded.")

    # create OCI clients
    oci_client_core = oci.core.ComputeClient(oci_configuration)

    # GET instance list
    instance_list = [
        instance.id
        for instance in oci.pagination.list_call_get_all_results(
            oci_client_core.list_instances,
            compartment_id=compartment_id
            ).data
        if (
            instance.lifecycle_state != "TERMINATED"
            and
            (
                instance.instance_options is None
                or
                'are_legacy_imds_endpoints_disabled' not in dir(instance.instance_options)
                or
                instance.instance_options.are_legacy_imds_endpoints_disabled is False
            )
        )
    ]

    # PATCH each instance
    for instance in instance_list:
        logging.info(f"OCI instance > updating {instance}")
        update_instance_response = oci_client_core.update_instance(
            instance_id=instance,
            update_instance_details=oci.core.models.UpdateInstanceDetails(
                instance_options=oci.core.models.InstanceOptions(are_legacy_imds_endpoints_disabled=True)
            )
        )

    logging.info("Successfully finished.")

if __name__ == "__main__":
  main()

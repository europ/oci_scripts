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
@click.option('-d', '--delete',
  help='Delete orphaned volumes.',
  required=False,
  type=bool,
  default=False,
  show_default=True,
  is_flag=True,
)
@click.help_option('-h', '--help')
def main(compartment_id, config_file, profile_name, delete):
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
    oci_client_core_compute = oci.core.ComputeClient(oci_configuration)
    oci_client_core_blockstorage = oci.core.BlockstorageClient(oci_configuration)

    # GET all attached volumes
    volume_attached_list = [
        volume.volume_id
        for volume in oci.pagination.list_call_get_all_results(
            oci_client_core_compute.list_volume_attachments,
            compartment_id=compartment_id
            ).data
    ]

    # GET all volumes
    volume_all_list = [
        volume.id
        for volume in oci.pagination.list_call_get_all_results(
            oci_client_core_blockstorage.list_volumes,
            compartment_id=compartment_id
            ).data
    ]

    # SELECT all orphaned volumes
    volume_orphaned_list = [
        volume_id
        for volume_id in volume_all_list
        if volume_id not in volume_attached_list
    ]

    # DELETE orphaned volumes
    if delete is True:
        for volume_id in volume_orphaned_list:
            logging.info(f"OCI block volume > deleting {volume_id}")
            update_instance_response = oci_client_core_blockstorage.delete_volume(
                volume_id=volume_id
            )

    logging.info("Successfully finished.")

if __name__ == "__main__":
  main()

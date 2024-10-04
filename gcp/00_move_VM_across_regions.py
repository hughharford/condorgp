from google.cloud import compute_v1


def get_instance(project_id: str, zone: str, instance_name: str) -> compute_v1.Instance:
    """
    Get information about a VM instance in the given zone in the specified project.

    Args:
        project_id: project ID or project number of the Cloud project you want to use.
        zone: name of the zone you want to use. For example: “us-west3-b”
        instance_name: name of the VM instance you want to query.
    Returns:
        An Instance object.
    """
    instance_client = compute_v1.InstancesClient()
    instance = instance_client.get(
        project=project_id, zone=zone, instance=instance_name
    )

    return instance

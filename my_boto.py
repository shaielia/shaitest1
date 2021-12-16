import boto3

client = boto3.client("ec2")


def get_instance_ids(client):
    my_instances = client.describe_instances()
    instance_ids_to_return = []
    for reservation in my_instances["Reservations"]:
        for instance in reservation["Instances"]:
            if instance["InstanceType"] == "t2.micro" and instance["State"]["Name"] == "running":
                instance_ids_to_return.append({"id": instance["InstanceId"], "ip": instance["PublicIpAddress"]})
    return instance_ids_to_return


ec2 = boto3.resource('ec2')

def create_instance(ec2):
    response = ec2.create_instances(SubnetId="subnet-018523f5b12a8b3fb", InstanceType="t2.micro", ImageId="ami-0947d2ba12ee1ff75", MaxCount=1, MinCount=1)
    return response

def stop_my_instance(client, instance_to_stop):
    response = client.stop_instances(InstanceIds=[instance_to_stop])
    return response

# create_instance(ec2)
print(get_instance_ids(client))
# stop_my_instance(client, "i-0e498ecccade1943e")

def set_eip_by_instance_id(client, instance_id):
    allocation = client.allocate_address()
    response = client.associate_address(AllocationId=allocation['AllocationId'], InstanceId=instance_id)
    return response

set_eip_by_instance_id(client, "i-0e498ecccade1943e")
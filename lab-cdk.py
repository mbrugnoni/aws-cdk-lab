from constructs import Construct
from aws_cdk import (
    App,
    Stack,
    aws_ec2 as ec2,
)

class VPCStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Create a VPC
        vpc = ec2.Vpc(self, "Lab-VPC",
                      max_azs=2,
                      cidr="10.0.0.0/16",
                      subnet_configuration=[
                          ec2.SubnetConfiguration(
                              subnet_type=ec2.SubnetType.PUBLIC,
                              name="Public",
                              cidr_mask=24
                          )
                          
                      ],
                      nat_gateways=0
                      )

        # Create a security group
        security_group = ec2.SecurityGroup(self, "SecurityGroup",
                                            vpc=vpc,
                                            description="Allow SSH access",
                                            allow_all_outbound=True
                                            )
        security_group.add_ingress_rule(ec2.Peer.any_ipv4(), ec2.Port.tcp(22), "Allow SSH access")

        # Create an EC2 instance
        instance_type = ec2.InstanceType("t2.micro")
        instance = ec2.Instance(self, "LinuxSandbox1",
                                instance_type=instance_type,
                                machine_image=ec2.MachineImage.latest_amazon_linux(),
                                vpc=vpc,
                                security_group=security_group
                                )

app = App()
VPCStack(app, "LabStack")
app.synth()

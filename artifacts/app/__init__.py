from aws_cdk import (
    core,
    aws_ec2 as ec2,
    aws_iam as iam,
)

with open("./artifacts/app/user_data.sh") as f:
    user_data = f.read()

class Ec2(core.NestedStack):

    def __init__(self, scope: core.Construct, id: str, bmt_vpc: ec2.Vpc, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        instance_role = iam.Role(self, 'controller-role',
            role_name='instance-role',
            managed_policies=[
                iam.ManagedPolicy.from_managed_policy_arn(self,'ssm_instance_core','arn:aws:iam::aws:policy/AmazonSSMManagedInstanceCore'),
                iam.ManagedPolicy.from_managed_policy_arn(self,'cloudwatch_agnet','arn:aws:iam::aws:policy/CloudWatchAgentServerPolicy')
            ],
            assumed_by=iam.ServicePrincipal('ec2.amazonaws.com')
        )

        ec2.Instance(self, 'controller',
            instance_type=ec2.InstanceType(instance_type_identifier="t3.micro"),
            machine_image=ec2.AmazonLinuxImage(generation=ec2.AmazonLinuxGeneration.AMAZON_LINUX_2),
            instance_name="controller",
            role=instance_role,
            vpc=bmt_vpc,
            vpc_subnets=ec2.SubnetSelection(subnet_type=ec2.SubnetType.PUBLIC),
            user_data=ec2.UserData.custom(user_data)
        )

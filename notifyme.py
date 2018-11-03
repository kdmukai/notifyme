import argparse
import configparser
import sys

import boto3


parser = argparse.ArgumentParser(description='Crypto Simple Trading Bot')

parser.add_argument(dest="target_phrase",
                    help="input in quotes")

parser.add_argument('-c', '--settings',
                    default="conf/settings_local.conf",
                    dest="settings_config",
                    help="Override default settings config file location")


if __name__ == "__main__":
    args = parser.parse_args()

    # Read settings
    arg_config = configparser.SafeConfigParser()
    arg_config.read(args.settings_config)

    target_phrase = args.target_phrase

    host = arg_config.get('LOCAL', 'HOST')

    sns_topic = arg_config.get('AWS', 'SNS_TOPIC')
    aws_access_key_id = arg_config.get('AWS', 'AWS_ACCESS_KEY_ID')
    aws_secret_access_key = arg_config.get('AWS', 'AWS_SECRET_ACCESS_KEY')

    # Prep boto SNS client for email notifications
    sns = boto3.client(
        "sns",
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        region_name="us-east-1"     # N. Virginia
    )


    for line in sys.stdin:
        if target_phrase in line:
            print("TARGET PHRASE! %s" % line)
            msg = line[line.index(target_phrase):]
            sns.publish(Message="%s: %s" % (host, msg), TopicArn=sns_topic)
        else:
            sys.stdout.write(line)


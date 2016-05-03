import requests
import ast
import re
import uuid
from urlparse import urljoin
from st2actions.runners.pythonrunner import Action


class CloudFormationSpec(Action):
    def run(self, payload, config):
        # take the payload name and replace any non-alphanumerical characters with "-"
        try:
            db_name = re.sub('[^0-9a-zA-Z]+', '-', payload['name']) + "-" + payload['namespace']
        except:
            self.logger.exception('Cannot create valid name for database!')
            raise

        # Lets get a username generated
        uid = payload.get('uid', None)
        if not uid:
            msg = 'No name or namespace in payload.'
            self.logger.error(msg)
            raise Exception(msg)

        user_name = self._user_name(uid=uid)

        pw = self._id_generator()        # to create a name for the database

        try:
            stack_name = stack_name_or_id = payload['labels']['stack_name']
            s3_bucket_url = self.config.get('s3_bucket_url')
            template_filename = payload['labels']['template_filename']
            parameter_filename = payload['labels']['parameter_filename']
            namespace = payload['namespace']
            template_url = urljoin(s3_bucket_url, template_filename)
            parameter_url = urljoin(s3_bucket_url, parameter_filename)
            parameters = ast.literal_eval(requests.get(parameter_url).text)

        except:
            self.logger.exception('Cannot create valid name for Cloudformation Stack!')
            raise

        l = dict(self.config.get('cloudformation', {}))

        newpayload = {
            'stack_name': stack_name,
            'stack_name_or_id': stack_name,
            'template_url': template_url,
            'parameters': parameters,
            'namespace': namespace,
            'db_name': db_name,
            'user_name': user_name,
            'pw': pw
        }

        # Parse through config.yaml for cloudformation:. If cloudformation.key exists in labels.keys(),
        # use label.value otherwise use default value from config.yaml
        # then add to newpayload dict.
        for i in l:
            if i in payload['labels']:
                key = i
                value = payload['labels'][i]
                newpayload[key] = value
            else:
                key = i
                valuealt = l[i]
                newpayload[key] = valuealt

        return newpayload

    def _user_name(self, uid):
        short_uid = uid[0:7]
        return "db_" + short_uid

    def _id_generator(self):
        return uuid.uuid4().hex

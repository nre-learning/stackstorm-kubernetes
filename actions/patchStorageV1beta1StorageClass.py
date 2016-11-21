from lib import k8s

from st2actions.runners.pythonrunner import Action

class patchStorageV1beta1StorageClass(Action):

    def run(self,body,name,pretty=None):

        myk8s = k8s.K8sClient(self.config)

        args = {}
        if body is not None:
          args['body'] = body
        if name is not None:
          args['name'] = name
        if pretty is not None:
          args['pretty'] = pretty

        return myk8s.runAction('patchStorageV1beta1StorageClass', **args)
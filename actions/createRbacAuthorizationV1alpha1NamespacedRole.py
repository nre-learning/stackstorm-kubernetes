from lib import k8s

from st2actions.runners.pythonrunner import Action

class createRbacAuthorizationV1alpha1NamespacedRole(Action):

    def run(self,body,namespace,pretty=None):

        myk8s = k8s.K8sClient(self.config)

        args = {}
        if body is not None:
          args['body'] = body
        if namespace is not None:
          args['namespace'] = namespace
        if pretty is not None:
          args['pretty'] = pretty

        return myk8s.runAction('createRbacAuthorizationV1alpha1NamespacedRole', **args)
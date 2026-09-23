"""Tests for the command patterns in validate.py.

Usage: python -m unittest discover -s scripts
"""

import unittest

import validate


class MutatingTest(unittest.TestCase):
    def test_state_changing_commands_are_found(self):
        for line in [
            "kubectl delete pod x",
            "kubectl -n prod delete pod x",
            "kubectl --namespace prod rollout restart deploy/x",
            "kubectl --namespace=prod rollout undo deploy/x",
            "kubectl --context c -n prod scale deploy/x --replicas=0",
            "kubectl -n prod set image deploy/x app=img:1",
            "kubectl -n prod \\\n  delete pod x",
            "kubectl get pods && kubectl -n prod exec -it x -- sh",
            "krci pipelinerun start build-pipeline",
            "krci run start build-pipeline",
            "krci project build orders --branch main",
            "krci proj build orders",
            "krci -o json project build orders",
            "tkn pipeline start build",
            "tkn -n ns pipelinerun delete x",
            "helm -n prod upgrade app chart",
            "argocd app sync shop-prod-orders",
            "git push origin main",
            "gh pr merge 1",
            "gh pr create --fill",
            "gh release create v1.0.0",
            "gh workflow run release.yml",
            "glab mr merge 1",
        ]:
            with self.subTest(line=line):
                self.assertTrue(validate.find_mutating(line), line)

    def test_read_only_commands_are_not_found(self):
        for line in [
            "kubectl get pods -n prod",
            "kubectl -n prod describe pod x",
            "kubectl -n prod logs deploy/x --previous",
            "kubectl auth can-i delete pods -n prod",
            "kubectl get events --field-selector reason=Failed",
            "kubectl rollout status deploy/x",
            "kubectl rollout history deploy/x",
            "krci pipelinerun list --project orders --status failed --reason",
            "krci project build --help",
            "krci project build orders --branch main --dry-run -o yaml",
            "krci pipelinerun start build-pipeline --dry-run",
            "kubectl -n prod delete pod x --dry-run=server",
            "krci project list -o json",
            "tkn pipelinerun logs x",
            "helm -n prod history app",
            "argocd app get shop-prod-orders",
            "git log --oneline",
            "gh pr view 1",
            "gh release view v1.0.0",
        ]:
            with self.subTest(line=line):
                self.assertFalse(validate.find_mutating(line), line)


class SecretDumpTest(unittest.TestCase):
    def test_secret_dumps_are_found(self):
        for line in [
            "kubectl get secret s -o yaml",
            "kubectl -n ns get secrets -o json",
            "kubectl get secret s --output=json",
            "kubectl get secret s -o go-template='{{.data}}'",
            "kubectl get secret s -o template --template='{{.data}}'",
            "kubectl get secret s -o jsonpath='{.data.token}'",
            "kubectl view-secret s",
            "echo $X | base64 -d",
        ]:
            with self.subTest(line=line):
                self.assertTrue(validate.find_secret_dumps(line), line)

    def test_key_listing_is_allowed(self):
        for line in [
            "kubectl get secret s",
            "kubectl get secret s -o json | jq '.data | keys'",
            "kubectl describe secret s",
            "kubectl get secret s -o jsonpath='{.data.\\.dockerconfigjson}' | base64 -d | jq '.auths | keys'",
        ]:
            with self.subTest(line=line):
                self.assertFalse(validate.find_secret_dumps(line), line)


class ParseListTest(unittest.TestCase):
    def test_valid_values(self):
        self.assertEqual(validate.parse_list("dev, qa", validate.ROLE_VALUES), ({"dev", "qa"}, []))
        self.assertEqual(validate.parse_list("all", validate.ROLE_VALUES), ({"all"}, []))

    def test_invalid_values(self):
        for value in ["", "all, dev", "dev, tester", "dev, dev"]:
            with self.subTest(value=value):
                self.assertTrue(validate.parse_list(value, validate.ROLE_VALUES)[1], value)


if __name__ == "__main__":
    unittest.main()

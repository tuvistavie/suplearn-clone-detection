import json

from tests.base import TestCase

from suplearn_clone_detection import ast


class AstTest(TestCase):
    @classmethod
    def setUpClass(cls):
        with open(cls.fixture_path("asts.json")) as f:
            cls.asts = [json.loads(v) for v in f if v]

    def test_from_list_without_value(self):
        list_ast = [{"type": "foo"}]
        root = ast.from_list(list_ast)
        self.assertEqual(root.type, "foo")
        self.assertIsNone(root.value)
        self.assertEqual(len(root.children), 0)

    def test_from_list_with_value(self):
        list_ast = [{"type": "foo", "value": "bar"}]
        root = ast.from_list(list_ast)
        self.assertEqual(root.type, "foo")
        self.assertEqual(root.value, "bar")
        self.assertEqual(len(root.children), 0)

    def test_from_list_recursive(self):
        list_ast = [{"type": "foo", "value": "bar", "children": [1]},
                    {"type": "baz"}]
        root = ast.from_list(list_ast)
        self.assertEqual(root.type, "foo")
        self.assertEqual(root.value, "bar")
        self.assertEqual(len(root.children), 1)
        child = root.children[0]
        self.assertEqual(child.type, "baz")

    def test_from_list_complex(self):
        list_ast = self.asts[0]
        root = ast.from_list(list_ast)
        self.assertEqual(root.type, "CompilationUnit")

    def test_dfs(self):
        list_ast = self.asts[0]
        root = ast.from_list(list_ast)
        bfs_types = [node.type for node in root.dfs()]
        expected = [node["type"] for node in list_ast]
        self.assertEqual(bfs_types, expected)

    def test_dfs_reverse(self):
        list_ast = self.asts[0]
        root = ast.from_list(list_ast)
        reversed_bfs_types = [node.type for node in root.dfs(reverse=True)]
        not_expected = [node["type"] for node in list_ast]
        self.assertNotEqual(reversed_bfs_types, not_expected)
        self.assertEqual(reversed_bfs_types[1], "ClassOrInterfaceDeclaration")
        self.assertEqual(reversed_bfs_types[2], "MethodDeclaration")

    def _load_list_ast(self):
        with open(self.fixture_path("asts.json")) as f:
            return json.loads(next(f))

# Tests directives

[odoo documentation](https://www.odoo.com/documentation/16.0/fr/developer/reference/backend/testing.html)

We use a [separate module](https://github.com/odoo/odoo/issues/40188) for the tests in order to import other modules.
The odoo_graphql doesn't had any data that can be used for efficient tests



```bash
python3.8 git/Odoo/odoo/odoo-bin -c configs/graphql.conf -d graphql --test-enable --test-tags /odoo_graphql_test -i odoo_graphql_test --stop-after-init
```

* Create database `graphql` if not exists
* install module `odoo_graphql`
* run all tests



We can also run test on update and for specific modules

> \[-]\[tag]\[/module]\[:class]\[.method]

```bash
python3.8 git/Odoo/odoo/odoo-bin -c configs/graphql.conf -d graphql --test-enable --test-tags /odoo_graphql_test -u odoo_graphql_test --stop-after-init
```





### Assertions

This is a list of assertions found in Odoo's code, they can be accessed in test through `self`

```python
self.assertTrue(value)
```

* **assertTrue**

* **assertFalse**

* **assertIsNone**

* **assertEqual**

* **assertAlmostEqual**

* **assertListEqual**

* **assertDictEqual**

* **assertGreater**

* **assertLess**

* **assertOrder**

* **assertIn**

* **assertNotIn**

* **assertRecordValues**

* **assertRaises**

  ```python
  with self.assertRaises(ValidationError):
  	# Code that must raise
      ...
  ```

  

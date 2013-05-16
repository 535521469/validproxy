[2013-05-16 v0.0.2]
1.验证代理时，如果发生重定向，一律看作是代理不可用。即使用代理得到的url地址是被代理封装后的url。

[2013-04-27 v0.0.1]
1.get proxy list from db
2.if request fail or retry for many time and eventually fail , modify status to invalid
3.when get the response , change status to valid
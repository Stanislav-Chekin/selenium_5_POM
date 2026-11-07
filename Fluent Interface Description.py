getter (void) == const
void, bool, status_code action (params) != const

mydb = MSDBEngine()
mydb.action1(params)
mydb.action2(other_params)
mydb.action3(third_params)

Fluent Interface Implementation
this, self || looks like self action (params) != const

mydb = MSDBEngine()
mydb.action1(params).action2(other_params).action3(third_params)


mydb.action1(params).action2(other_params).action3(third_params);
mydb.action1(params).
    action2(other_params).
    action3(third_params);

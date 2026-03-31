| Perfil | Operativo | Scope permitido | Cardinalidad | Puede coexistir con |
| --- | --- | --- | --- | --- |
| Operación | sí | branch | exactamente 1 sucursal | Supervisión, Gerencia |
| Administración sucursal | sí | branch | exactamente 1 sucursal | Supervisión, Gerencia, eventualmente Operación |
| Supervisión | no | branch, branch\_set, global | 1, varias o todas | todos, mientras no altere la sucursal operativa |
| Gerencia | no | branch\_set, global | varias o global | todos |
| Sistema | no | global | global | restringido, según política interna |




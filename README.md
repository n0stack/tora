# N0stack-Tora

## Requirement
### ubuntu package
- kvm
- virt-manager
- libvirt-bin
- bridge-utils
- libvirt-dev

## API Docs

### GET
#### `/vm`
Get all vm's information.

#### `/vm/<vm_name>`
Get <vm_name>'s information.

#### `/pool`
Get all pool's information.

#### `/pool/<pool_name>`
Get <pool_name>'s information.


### POST
#### `/vm`
- post_info:
```
{
	"name":"example"
}
```

### PUT
#### `/vm/vm_name`
- put_info:
```
{
	"name":"example"
}
```

### DELETE
#### `/vm/<vm_name>`
Delete <vm_name>.


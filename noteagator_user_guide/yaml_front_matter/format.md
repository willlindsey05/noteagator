---
description: How to define note format
---
Notes can include a `format` key in their YAML front matter to control how they are displayed when printed.  
The avaliable formats are:  
|Format|Behavior|
|---|---|
|`markdown`|Prints the note in markdown formatting|
|`slim`|Prints the note without markdown formatting and takes up less space|  

**Example**  
```yaml
---
description: Slim output example
format: slim
---
code 1
'''
code block
'''
```  
When Printed  
```console
$ ngt print 3
code 1
--copy 1 $ code block

```
# Installation

## Maven:

### GroupId pattern:
- base: com.bstn
    - app: com.bstn.app
    - util: com.bstn.util
    - module: com.bstn.module

### Install Repository pattern:
mvn install:install-file -Dfile=<path>\lib\<name>.jar -DgroupId=<GroupId> -DartifactId=<ArtifactId> -Dversion=<version> -Dpackaging=jar


### Home Desktop:
- coreutil:
    $ mvn install:install-file -Dfile=C:\Users\JerBa\Desktop\synka\PDFUtil\Java\eclipse-workspace\CLI\lib\coreutil.jar -DgroupId=com.bstn.util -DartifactId=coreutil -Dversion=0.1.6 -Dpackaging=jar

- pdfboxutil:
    $ mvn install:install-file -Dfile=C:\Users\JerBa\Desktop\synka\PDFUtil\Java\eclipse-workspace\CLI\lib\pdfboxutil.jar -DgroupId=com.bstn.util -DartifactId=pdfboxutil -Dversion=0.0.4 -Dpackaging=jar

- search:
    $ mvn install:install-file -Dfile=C:\Users\JerBa\Desktop\synka\PDFUtil\Java\eclipse-workspace\CLI\lib\search.jar -DgroupId=com.bstn.module -DartifactId=search -Dversion=0.0.6 -Dpackaging=jar



### General

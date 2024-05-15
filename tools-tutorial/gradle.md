
### Java compilation errors limited to 100

gradle/helper/compile.gradle

给options.compilerArgs设置-Xmaxerrs

```
configure(javaprojects) {
  compileJava {
    sourceCompatibility = JavaVersion.VERSION_17
    targetCompatibility = JavaVersion.VERSION_17
    options.encoding = 'UTF-8'
    options.compilerArgs << "-Xlint:-cast,-deprecation,-rawtypes,-try,-unchecked,-processing" << '-Xmaxerrs' << '100000'

    doLast {
      if (project.name == 'keta-server') {
        project.file('build/runtime').deleteDir()
        copy { into(project.file('build/runtime')) from(project.sourceSets.main.runtimeClasspath) }
      }
    }
  }

  compileTestJava {
    options.encoding = 'UTF-8'
    options.compilerArgs << "-Xlint:-cast,-deprecation,-rawtypes,-try,-unchecked"
  }
}
```


## REF

- https://stackoverflow.com/questions/3115537/java-compilation-errors-limited-to-100
- https://stackoverflow.com/questions/31792765/gradle-build-finished-with-200-errors-change-limit-in-android-studio
- https://stackoverflow.com/questions/76264497/set-xmaxerros-and-xmaxwarns-in-gradle-to-display-all-errorprone-messages


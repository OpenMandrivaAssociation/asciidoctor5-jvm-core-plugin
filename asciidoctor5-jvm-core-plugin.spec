Name:		asciidoctor5-jvm-core-plugin
Version:	5.1.0
Release:	1
Summary:	AsciidoctorJ Gradle plugins
Group:		Development/Java
License:	Apache-2.0
URL:		https://github.com/asciidoctor/asciidoctor-gradle-plugin
# Tag release_5_1_0, model5/jvm-core only. The Gradle tool is not
# invoked. Sources are compiled with Groovy's FileSystemCompiler at
# class version 61. Patch0 replaces Collections.EMPTY_LIST with a
# typed emptyList so Groovy 4 static type checking accepts
# ListProperty.convention.
Source0:	asciidoctor5-jvm-core-plugin-%{version}.tar.gz
Patch0:	asciidoctor5-jvm-core-plugin-groovy4-stc.patch

BuildArch:	noarch
BuildRequires:	java-current-devel
BuildRequires:	apache-groovy
BuildRequires:	antlr4
BuildRequires:	objectweb-asm
BuildRequires:	picocli
BuildRequires:	jansi
BuildRequires:	ant-lib
BuildRequires:	gradle
BuildRequires:	mvn(org.asciidoctor:asciidoctor5-core-plugin) = 5.1.0
BuildRequires:	mvn(org.ysb33r.gradle:grolifant5-core) = 5.12.7
BuildRequires:	mvn(org.ysb33r.gradle:grolifant5-herd) = 5.12.7
BuildRequires:	mvn(org.ysb33r.gradle:grolifant5-rawhide) = 5.12.7
BuildRequires:	mvn(org.asciidoctor:asciidoctorj) = 3.0.1
BuildRequires:	mvn(org.asciidoctor:asciidoctorj-api) = 3.0.1
BuildRequires:	mvn(org.asciidoctor:asciidoctorj-groovy-dsl) = 3.0.0.beta.2
BuildRequires:	mvn(org.ysb33r.gradle.jruby:jrubygradle-resolver) = 3.0.0
BuildRequires:	mvn(org.jruby:jruby) = 9.4.14.0
BuildRequires:	mvn(javax.inject:javax.inject)
BuildRequires:	sysjar
BuildRequires:	javapackages-filesystem
Requires:	apache-groovy
Requires:	gradle

%description
org.asciidoctor:asciidoctor5-jvm-core-plugin %{version}. ErbEngine.from
parses an eRuby engine name and getOptionValue returns the lowercase
option. The Gradle tool is not invoked.

%prep
%autosetup -n asciidoctor5-jvm-core-plugin-%{version} -p1
find . -type f \( -name '*.jar' -o -name '*.class' -o -name '*.so' -o -name '*.node' -o -name '*.wasm' \) -print > binaries.list
find . -type d -name '*.jar' -print >> binaries.list
if [ -s binaries.list ]; then
	cat binaries.list
	exit 1
fi
find model5/jvm-core/src/main -type f \( -name '*.groovy' -o -name '*.java' \) | sort > sources.list
test "$(wc -l < sources.list)" -eq 69
test "$(grep -c '\.groovy$' sources.list)" -eq 46
test "$(grep -c '\.java$' sources.list)" -eq 23
grep -F -q 'Collections.<String>emptyList()' \
	model5/jvm-core/src/main/groovy/org/asciidoctor/gradle/model5/jvm/internal/toolchains/DefaultAsciidoctorjToolchain.groovy
if grep -F -q 'import static java.util.Collections.EMPTY_LIST' \
	model5/jvm-core/src/main/groovy/org/asciidoctor/gradle/model5/jvm/internal/toolchains/DefaultAsciidoctorjToolchain.groovy
then
	exit 1
fi
props=model5/jvm-core/src/main/resources/META-INF/asciidoctor.gradle/asciidoctor5-jvm-core-plugin.properties
sed -i \
	-e 's/@@BATIK@@/1.19/' \
	-e 's/@@DIAGRAM@@/3.2.1/' \
	-e 's/@@DITAA@@/1.0.3/' \
	-e 's/@@EPUB@@/2.2.0/' \
	-e 's/@@GROOVYDSL@@/3.0.0-beta.2/' \
	-e 's/@@HAML@@/6.3.0/' \
	-e 's/@@JRUBY@@/9.4.8.0/' \
	-e 's/@@JSYNTRAX@@/1.38.2/' \
	-e 's/@@KROKI@@/0.10.0/' \
	-e 's/@@PDF@@/2.3.23/' \
	-e 's/@@PLANTUML@@/1.2026.2/' \
	-e 's/@@REVEALJS@@/5.2.0/' \
	-e 's/@@SLIM@@/5.2.1/' \
	-e 's/@@TILT@@/2.6.1/' \
	-e 's/@@VERSION@@/3.0.1/' \
	"$props"
grep -F -q 'asciidoctorj=3.0.1' "$props"
grep -F -q 'jruby=9.4.8.0' "$props"
grep -F -q 'asciidoctorj.groovydsl=3.0.0-beta.2' "$props"
if grep -F '@@' "$props"; then
	exit 1
fi

%build
set -eo pipefail
export JAVA_HOME=%{_jvmdir}/java-openjdk
export PATH="$JAVA_HOME/bin:$PATH"
tool_cp=%{_javadir}/apache-groovy.jar
for extra in \
	%{_javadir}/apache-groovy-xml.jar \
	%{_javadir}/apache-groovy-json.jar \
	%{_javadir}/apache-groovy-templates.jar \
	%{_javadir}/antlr4-runtime.jar \
	%{_javadir}/asm.jar \
	%{_javadir}/asm-commons.jar \
	%{_javadir}/asm-tree.jar \
	%{_javadir}/asm-util.jar \
	%{_javadir}/asm-analysis.jar \
	%{_javadir}/picocli.jar \
	/usr/lib/java/jansi/jansi.jar \
	%{_javadir}/ant.jar
do
	test -s "$extra"
	tool_cp=$tool_cp:$extra
done
src_cp=%{_javadir}/jruby.jar
for extra in \
	%{_javadir}/grolifant5-core.jar \
	%{_javadir}/grolifant5-herd.jar \
	%{_javadir}/grolifant5-rawhide.jar \
	%{_javadir}/asciidoctor5-core-plugin.jar \
	%{_javadir}/asciidoctoreditorconfig.jar \
	%{_javadir}/asciidoctorj-api.jar \
	%{_javadir}/asciidoctorj.jar \
	%{_javadir}/asciidoctorj-groovy-dsl.jar \
	%{_javadir}/jrubygradle-resolver.jar \
	%{_javadir}/atinject.jar \
	%{_javadir}/apache-groovy.jar
do
	test -s "$extra"
	src_cp=$src_cp:$extra
done
for dir in %{_datadir}/gradle/lib %{_datadir}/gradle/lib/plugins %{_datadir}/gradle/lib/agents; do
	if [ -d "$dir" ]; then
		for j in "$dir"/*.jar; do
			if [ -s "$j" ]; then
				src_cp=$src_cp:$j
			fi
		done
	fi
done
mkdir -p classes
java -Dgroovy.target.bytecode=17 -cp "$tool_cp" org.codehaus.groovy.tools.FileSystemCompiler \
	--classpath "$src_cp" -j '-J-release=17' -d classes @sources.list
test "$(find classes -name '*.class' | wc -l)" -eq 164
javap -v -classpath classes org.asciidoctor.gradle.model5.jvm.engines.ErbEngine | grep -F -q 'major version: 61'
javap -v -classpath classes org.asciidoctor.gradle.model5.jvm.plugins.AsciidoctorjPlugin | grep -F -q 'major version: 61'
/bin/cp -a model5/jvm-core/src/main/resources/META-INF classes/
mkdir -p classes/META-INF/gradle-plugins
printf '%s\n' 'implementation-class=org.asciidoctor.gradle.model5.jvm.plugins.AsciidoctorjBasePlugin' \
	> classes/META-INF/gradle-plugins/org.asciidoctor.jvm.base.properties
printf '%s\n' 'implementation-class=org.asciidoctor.gradle.model5.jvm.plugins.AsciidoctorjPlugin' \
	> classes/META-INF/gradle-plugins/org.asciidoctor.jvm.properties
printf '%s\n' 'implementation-class=org.asciidoctor.gradle.model5.jvm.plugins.AsciidoctorjPdfPlugin' \
	> classes/META-INF/gradle-plugins/org.asciidoctor.jvm.pdf.properties
printf '%s\n' 'implementation-class=org.asciidoctor.gradle.model5.jvm.plugins.AsciidoctorjRevealjsPlugin' \
	> classes/META-INF/gradle-plugins/org.asciidoctor.jvm.revealjs.properties
printf '%s\n' 'implementation-class=org.asciidoctor.gradle.model5.jvm.plugins.AsciidoctorjGemsPlugin' \
	> classes/META-INF/gradle-plugins/org.asciidoctor.jvm.gems.properties
printf '%s\n' 'implementation-class=org.asciidoctor.gradle.model5.jvm.plugins.AsciidoctorjDiagramPlugin' \
	> classes/META-INF/gradle-plugins/org.asciidoctor.jvm.diagram.properties
printf '%s\n' 'implementation-class=org.asciidoctor.gradle.model5.jvm.plugins.AsciidoctorjKrokiPlugin' \
	> classes/META-INF/gradle-plugins/org.asciidoctor.jvm.kroki.properties
printf '%s\n' 'implementation-class=org.asciidoctor.gradle.model5.jvm.plugins.AsciidoctorjEpubPlugin' \
	> classes/META-INF/gradle-plugins/org.asciidoctor.jvm.epub.properties
grep -F -q 'asciidoctorj=3.0.1' classes/META-INF/asciidoctor.gradle/asciidoctor5-jvm-core-plugin.properties
printf '%s\n' 'Manifest-Version: 1.0' 'Automatic-Module-Name: org.asciidoctor.asciidoctor5.jvm.core.plugin' > manifest.mf
jar cfm asciidoctor5-jvm-core-plugin.jar manifest.mf -C classes .
jar i asciidoctor5-jvm-core-plugin.jar
jar tf asciidoctor5-jvm-core-plugin.jar | grep -F -q 'org/asciidoctor/gradle/model5/jvm/engines/ErbEngine.class'
jar tf asciidoctor5-jvm-core-plugin.jar | grep -F -q 'META-INF/gradle-plugins/org.asciidoctor.jvm.properties'
jar tf asciidoctor5-jvm-core-plugin.jar | grep -F -q 'META-INF/asciidoctor.gradle/asciidoctor5-jvm-core-plugin.properties'
jar --describe-module --file asciidoctor5-jvm-core-plugin.jar > describe.txt
if grep -F -q 'Unable' describe.txt; then
	cat describe.txt
	exit 1
fi
grep -F -qx 'org.asciidoctor.asciidoctor5.jvm.core.plugin automatic' describe.txt

cat > asciidoctor5-jvm-core-plugin.pom << 'END'
<project>
  <modelVersion>4.0.0</modelVersion>
  <groupId>org.asciidoctor</groupId>
  <artifactId>asciidoctor5-jvm-core-plugin</artifactId>
  <version>%{version}</version>
  <name>asciidoctor5-jvm-core-plugin</name>
  <licenses>
    <license>
      <name>Apache-2.0</name>
    </license>
  </licenses>
  <dependencies>
    <dependency>
      <groupId>org.asciidoctor</groupId>
      <artifactId>asciidoctor5-core-plugin</artifactId>
      <version>5.1.0</version>
    </dependency>
    <dependency>
      <groupId>org.ysb33r.gradle</groupId>
      <artifactId>grolifant5-core</artifactId>
      <version>5.12.7</version>
    </dependency>
    <dependency>
      <groupId>org.ysb33r.gradle</groupId>
      <artifactId>grolifant5-herd</artifactId>
      <version>5.12.7</version>
    </dependency>
    <dependency>
      <groupId>org.ysb33r.gradle</groupId>
      <artifactId>grolifant5-rawhide</artifactId>
      <version>5.12.7</version>
    </dependency>
    <dependency>
      <groupId>org.ysb33r.gradle.jruby</groupId>
      <artifactId>jrubygradle-resolver</artifactId>
      <version>3.0.0</version>
    </dependency>
    <dependency>
      <groupId>org.asciidoctor</groupId>
      <artifactId>asciidoctorj</artifactId>
      <version>3.0.1</version>
    </dependency>
    <dependency>
      <groupId>org.asciidoctor</groupId>
      <artifactId>asciidoctorj-groovy-dsl</artifactId>
      <version>3.0.0.beta.2</version>
    </dependency>
  </dependencies>
</project>
END

%install
set -eo pipefail
sysjar install --buildroot %{buildroot} \
	--artifact asciidoctor5-jvm-core-plugin.pom:asciidoctor5-jvm-core-plugin.jar \
	--file-name asciidoctor5-jvm-core-plugin \
	--filelist .mfiles
idx="%{buildroot}/usr/share/sysjar/index/org.asciidoctor/asciidoctor5-jvm-core-plugin.sysjar"
test -s "$idx"
grep -F -q '"version": "%{version}"' "$idx"
grep -F -q '"artifactId": "asciidoctor5-jvm-core-plugin"' "$idx"
test -s %{buildroot}%{_javadir}/asciidoctor5-jvm-core-plugin.jar

%check
set -eo pipefail
export JAVA_HOME=%{_jvmdir}/java-openjdk
export PATH="$JAVA_HOME/bin:$PATH"
JAR=%{buildroot}%{_javadir}/asciidoctor5-jvm-core-plugin.jar
test -s "$JAR"
mkdir -p check
cat > check/JvmCoreCheck.java << 'EOF'
import org.asciidoctor.gradle.model5.jvm.engines.ErbEngine;

public class JvmCoreCheck {
    public static void main(String[] args) {
        ErbEngine engine = ErbEngine.from("erubi");
        if (engine != ErbEngine.ERUBI || !"erubi".equals(engine.getOptionValue())) {
            throw new RuntimeException(engine + " " + engine.getOptionValue());
        }
        System.out.println("jvm_core_ok erubi");
    }
}
EOF
"$JAVA_HOME/bin/javac" --release 17 -encoding UTF-8 -Xlint:-options -cp "$JAR" -d check check/JvmCoreCheck.java
"$JAVA_HOME/bin/java" -cp "check:$JAR" JvmCoreCheck > check/out.txt
cat check/out.txt
grep -F -qx 'jvm_core_ok erubi' check/out.txt

%files -f .mfiles
%doc README.adoc
%license LICENSE

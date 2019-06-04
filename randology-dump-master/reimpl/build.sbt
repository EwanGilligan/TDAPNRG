lazy val root = (project in file(".")).
  settings(
    name := "randology",
    version := "0.1.0",
    scalaVersion := "2.12.0",
    scalacOptions += "-feature",
    scalacOptions += "-deprecation",
    mainClass in Compile := 
      Some("uk.ac.stir.randology.experiments.Experiment1")
  )

resolvers += Resolver.sonatypeRepo("public")

libraryDependencies ++= Seq(
  //groupID % artifactID % revision
  "com.github.haifengl" % "smile-math" % "1.2.2",
  "org.slf4j" % "slf4j-simple" % "1.7.23",
  "org.scalacheck" % "scalacheck_2.12" % "1.13.4" % "test"
)

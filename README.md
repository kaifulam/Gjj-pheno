## Higgs Bosons and Machine Learning - Single b tagging

![Higgs Boson](http://cdn8.openculture.com/wp-content/uploads/2012/07/higgsboson.jpeg)

Higgs Bosons and Machine Learning... If you found this page, I'm sure you've at least watched a few youtube videos about these two things! You're a certified geek!

Before you dig into my codes, below are some good intuition refreshers...

**Higgs Bosons** - [Don Lincoln's 3 minute video](https://youtu.be/RIg1Vh7uPyw), [Sean Carroll on Great Course Plus](https://www.thegreatcoursesplus.com/the-higgs-boson-and-beyond/the-importance-of-the-higgs-boson) (It's worth the subscription fees!)

**Neural Network in Machine Learning** - [DeepLearning.TV series](https://youtu.be/b99UVkWzYTQ), [Andrew Ng on Coursera](https://www.coursera.org/learn/machine-learning)

The [7 detectors](https://home.cern/about/experiments) along the [Large Hadron Collider (LHC)](https://home.cern/topics/large-hadron-collider) are like big data generators. The LHC guide particles to smash against each other head on, and the detectors record all the bits and pieces that come out of it.

There're many smart people in CERN. (duh..) Some of them write algorithms to reconstruct trajectories of particles inside the detector. This is like tracing a [multiple head missile](https://en.wikipedia.org/wiki/Multiple_independently_targetable_reentry_vehicle#/media/File:Minuteman_III_MIRV_path.svg) backwards to the origin. The goal here is to identify the original particle (actually observed as [Jets](https://en.wikipedia.org/wiki/Jet_(particle_physics))) that creates all these mess in the detector based on a collection of trajectory variables.

This is where neural network comes in! We train the neural network by feeding in the variables of each jet, and give it the correct answer (say.. jet of a bottom quark). After seeing say.. 10 million examples, we see that the neural network model learn to identify particles, and it performs better than if we were to identify particles using each variable alone.

This is a follow on study of [this](https://arxiv.org/pdf/1607.08633.pdf) paper by [Dan Guest](https://github.com/dguest/delphes-rave/wiki/Output-Format)

Instructions to run the codes is [here](https://drive.google.com/file/d/0B3qwNGluXsHSUW9fdTNDRHh0LW8/view?usp=sharing)

Expert Level variables explained [here](https://drive.google.com/file/d/0B3qwNGluXsHSUW9fdTNDRHh0LW8/view?usp=sharing)


# Stackoverflow Crawler

A web crawler which crawls the **Stack Overflow** website. (Questions and Answers / Q&A)

[![stackoverflow](logo.png)](https://stackoverflow.com/)

### Try API

- https://stackoverflow.com/questions/tagged/c
- https://api.stackexchange.com/2.2/questions?order=desc&sort=activity&site=stackoverflow&pagesize=100
- https://api.stackexchange.com/2.2/questions/1163244?order=desc&sort=activity&site=askubuntu
- https://api.stackexchange.com/2.2/questions/1160229/answers?order=desc&sort=activity&site=askubuntu
- https://api.stackexchange.com/2.2/questions?order=desc&sort=activity&site=askubuntu&pagesize=100
- https://api.stackexchange.com/docs/questions

### Stack Exchange API

- https://api.stackexchange.com/
- https://api.stackexchange.com/docs
- https://stackapps.com/questions/7/how-to-list-your-application-library-wrapper-script-here
- http://stackapps.com/apps/oauth/register
- https://api.stackexchange.com/docs/throttle
- https://api.stackexchange.com/docs/authentication
- https://api.stackexchange.com/docs/write

-------

It's same as a fork and depends on some other projects on the GitHub:

- https://www.crummy.com/software/BeautifulSoup/bs4/doc/
- https://pypi.org/project/bs4/
- https://pypi.org/project/beautifulsoup4/
- https://www.crummy.com/software/BeautifulSoup/bs4/doc/#get-text
- https://github.com/topics/stackoverflow-crawler
- https://github.com/rjstyles/StackOverflow-Crawler
- https://github.com/topics/stackoverfolw-website
- ...

I did not remember that at now.

---------

## Testing

```
$ python3 craw.py
crawling page 1: https://stackoverflow.com/questions/tagged/c%2b%2b?sort=votes&page=1&pageSize=15
------------------------------
Why is processing a sorted array faster than processing an unsorted array?
<div class="post-text" itemprop="text">
<p>Here is a piece of C++ code that shows some very peculiar behavior. For some strange reason, sorting the data miraculously makes the code almost six times faster:</p>
<pre class="lang-cpp prettyprint-override"><code>#include &lt;algorithm&gt;
#include &lt;ctime&gt;
#include &lt;iostream&gt;

int main()
{
	// Generate data
	const unsigned arraySize = 32768;
	int data[arraySize];

	for (unsigned c = 0; c &lt; arraySize; ++c)
		data[c] = std::rand() % 256;


	// !!! With this, the next loop runs faster.
	std::sort(data, data + arraySize);


	// Test
	clock_t start = clock();
	long long sum = 0;

	for (unsigned i = 0; i &lt; 100000; ++i)
	{
		// Primary loop
		for (unsigned c = 0; c &lt; arraySize; ++c)
		{
			if (data[c] &gt;= 128)
				sum += data[c];
		}
	}

	double elapsedTime = static_cast&lt;double&gt;(clock() - start) / CLOCKS_PER_SEC;

	std::cout &lt;&lt; elapsedTime &lt;&lt; std::endl;
	std::cout &lt;&lt; "sum = " &lt;&lt; sum &lt;&lt; std::endl;
}
</code></pre>
<ul>
<li>Without <code>std::sort(data, data + arraySize);</code>, the code runs in 11.54 seconds.</li>
<li>With the sorted data, the code runs in 1.93 seconds.</li>
</ul>
<hr/>
<p>Initially I thought this might be just a language or compiler anomaly, so I tried Java:</p>
<pre class="lang-java prettyprint-override"><code>import java.util.Arrays;
import java.util.Random;

public class Main
{
	public static void main(String[] args)
	{
		// Generate data
		int arraySize = 32768;
		int data[] = new int[arraySize];

		Random rnd = new Random(0);
		for (int c = 0; c &lt; arraySize; ++c)
			data[c] = rnd.nextInt() % 256;


		// !!! With this, the next loop runs faster
		Arrays.sort(data);


		// Test
		long start = System.nanoTime();
		long sum = 0;

		for (int i = 0; i &lt; 100000; ++i)
		{
			// Primary loop
			for (int c = 0; c &lt; arraySize; ++c)
			{
				if (data[c] &gt;= 128)
					sum += data[c];
			}
		}

		System.out.println((System.nanoTime() - start) / 1000000000.0);
		System.out.println("sum = " + sum);
	}
}
</code></pre>
<p>with a similar but less extreme result.</p>
<hr/>
<p>My first thought was that sorting brings the data into the cache, but then I thought how silly that was because the array was just generated.</p>
<ul>
<li>What is going on?</li>
<li>Why is processing a sorted array faster than processing an unsorted array? The code is summing up some independent terms, so the order should not matter.</li>
</ul>
</div>
List of answers:


===>
Why is processing a sorted array faster than processing an unsorted array?

You are a victim of branch prediction fail.

What is Branch Prediction?
Consider a railroad junction:

Image by Mecanismo, via Wikimedia Commons. Used under the CC-By-SA 3.0 license.
Now for the sake of argument, suppose this is back in the 1800s - before long distance or radio communication.
You are the operator of a junction and you hear a train coming. You have no idea which way it is supposed to go. You stop the train to ask the driver which direction they want. And then you set the switch appropriately.
Trains are heavy and have a lot of inertia. So they take forever to start up and slow down.
Is there a better way? You guess which direction the train will go!

If you guessed right, it continues on.
If you guessed wrong, the captain will stop, back up, and yell at you to flip the switch. Then it can restart down the other path.

If you guess right every time, the train will never have to stop.
If you guess wrong too often, the train will spend a lot of time stopping, backing up, and restarting.

Consider an if-statement: At the processor level, it is a branch instruction:

You are a processor and you see a branch. You have no idea which way it will go. What do you do? You halt execution and wait until the previous instructions are complete. Then you continue down the correct path.
Modern processors are complicated and have long pipelines. So they take forever to "warm up" and "slow down".
Is there a better way? You guess which direction the branch will go!

If you guessed right, you continue executing.
If you guessed wrong, you need to flush the pipeline and roll back to the branch. Then you can restart down the other path.

If you guess right every time, the execution will never have to stop.
If you guess wrong too often, you spend a lot of time stalling, rolling back, and restarting.

This is branch prediction. I admit it's not the best analogy since the train could just signal the direction with a flag. But in computers, the processor doesn't know which direction a branch will go until the last moment.
So how would you strategically guess to minimize the number of times that the train must back up and go down the other path? You look at the past history! If the train goes left 99% of the time, then you guess left. If it alternates, then you alternate your guesses. If it goes one way every three times, you guess the same...
In other words, you try to identify a pattern and follow it. This is more or less how branch predictors work.
Most applications have well-behaved branches. So modern branch predictors will typically achieve >90% hit rates. But when faced with unpredictable branches with no recognizable patterns, branch predictors are virtually useless.
Further reading: "Branch predictor" article on Wikipedia.

As hinted from above, the culprit is this if-statement:
if (data[c] >= 128)
	sum += data[c];

Notice that the data is evenly distributed between 0 and 255. When the data is sorted, roughly the first half of the iterations will not enter the if-statement. After that, they will all enter the if-statement.
This is very friendly to the branch predictor since the branch consecutively goes the same direction many times. Even a simple saturating counter will correctly predict the branch except for the few iterations after it switches direction.
Quick visualization:
T = branch taken
N = branch not taken

data[] = 0, 1, 2, 3, 4, ... 126, 127, 128, 129, 130, ... 250, 251, 252, ...
branch = N  N  N  N  N  ...   N    N    T    T    T  ...   T    T    T  ...

	   = NNNNNNNNNNNN ... NNNNNNNTTTTTTTTT ... TTTTTTTTTT  (easy to predict)

However, when the data is completely random, the branch predictor is rendered useless, because it can't predict random data. Thus there will probably be around 50% misprediction (no better than random guessing).
data[] = 226, 185, 125, 158, 198, 144, 217, 79, 202, 118,  14, 150, 177, 182, 133, ...
branch =   T,   T,   N,   T,   T,   T,   T,  N,   T,   N,   N,   T,   T,   T,   N  ...

	   = TTNTTTTNTNNTTTN ...   (completely random - hard to predict)


So what can be done?
If the compiler isn't able to optimize the branch into a conditional move, you can try some hacks if you are willing to sacrifice readability for performance.
Replace:
if (data[c] >= 128)
	sum += data[c];

with:
int t = (data[c] - 128) >> 31;
sum += ~t & data[c];

This eliminates the branch and replaces it with some bitwise operations.
(Note that this hack is not strictly equivalent to the original if-statement. But in this case, it's valid for all the input values of data[].)
Benchmarks: Core i7 920 @ 3.5 GHz
C++ - Visual Studio 2010 - x64 Release
//  Branch - Random
seconds = 11.777

//  Branch - Sorted
seconds = 2.352

//  Branchless - Random
seconds = 2.564

//  Branchless - Sorted
seconds = 2.587

Java - NetBeans 7.1.1 JDK 7 - x64
//  Branch - Random
seconds = 10.93293813

//  Branch - Sorted
seconds = 5.643797077

//  Branchless - Random
seconds = 3.113581453

//  Branchless - Sorted
seconds = 3.186068823

Observations:

With the Branch: There is a huge difference between the sorted and unsorted data.
With the Hack: There is no difference between sorted and unsorted data.
In the C++ case, the hack is actually a tad slower than with the branch when the data is sorted.

A general rule of thumb is to avoid data-dependent branching in critical loops (such as in this example).

Update:

GCC 4.6.1 with -O3 or -ftree-vectorize on x64 is able to generate a conditional move. So there is no difference between the sorted and unsorted data - both are fast.
VC++ 2010 is unable to generate conditional moves for this branch even under /Ox.
Intel C++ Compiler (ICC) 11 does something miraculous. It interchanges the two loops, thereby hoisting the unpredictable branch to the outer loop. So not only is it immune the mispredictions, it is also twice as fast as whatever VC++ and GCC can generate! In other words, ICC took advantage of the test-loop to defeat the benchmark...
If you give the Intel compiler the branchless code, it just out-right vectorizes it... and is just as fast as with the branch (with the loop interchange).

This goes to show that even mature modern compilers can vary wildly in their ability to optimize code...

===>
Why is processing a sorted array faster than processing an unsorted array?

Branch prediction.
With a sorted array, the condition data[c] >= 128 is first false for a streak of values, then becomes true for all later values. That's easy to predict. With an unsorted array, you pay for the branching cost.

===>
Why is processing a sorted array faster than processing an unsorted array?

The reason why performance improves drastically when the data is sorted is that the branch prediction penalty is removed, as explained beautifully in Mysticial's answer.
Now, if we look at the code
if (data[c] >= 128)
	sum += data[c];

we can find that the meaning of this particular if... else... branch is to add something when a condition is satisfied. This type of branch can be easily transformed into a conditional move statement, which would be compiled into a conditional move instruction: cmovl, in an x86 system. The branch and thus the potential branch prediction penalty is removed.
In C, thus C++, the statement, which would compile directly (without any optimization) into the conditional move instruction in x86, is the ternary operator ... ? ... : .... So we rewrite the above statement into an equivalent one:
sum += data[c] >=128 ? data[c] : 0;

While maintaining readability, we can check the speedup factor.
On an Intel Core i7-2600K @ 3.4 GHz and Visual Studio 2010 Release Mode, the benchmark is (format copied from Mysticial):
x86
//  Branch - Random
seconds = 8.885

//  Branch - Sorted
seconds = 1.528

//  Branchless - Random
seconds = 3.716

//  Branchless - Sorted
seconds = 3.71

x64
//  Branch - Random
seconds = 11.302

//  Branch - Sorted
 seconds = 1.830

//  Branchless - Random
seconds = 2.736

//  Branchless - Sorted
seconds = 2.737

The result is robust in multiple tests. We get a great speedup when the branch result is unpredictable, but we suffer a little bit when it is predictable. In fact, when using a conditional move, the performance is the same regardless of the data pattern.
Now let's look more closely by investigating the x86 assembly they generate. For simplicity, we use two functions max1 and max2.
max1 uses the conditional branch if... else ...:
int max1(int a, int b) {
	if (a > b)
		return a;
	else
		return b;
}

max2 uses the ternary operator ... ? ... : ...:
int max2(int a, int b) {
	return a > b ? a : b;
}

On a x86-64 machine, GCC -S generates the assembly below.
:max1
	movl    %edi, -4(%rbp)
	movl    %esi, -8(%rbp)
	movl    -4(%rbp), %eax
	cmpl    -8(%rbp), %eax
	jle     .L2
	movl    -4(%rbp), %eax
	movl    %eax, -12(%rbp)
	jmp     .L4
.L2:
	movl    -8(%rbp), %eax
	movl    %eax, -12(%rbp)
.L4:
	movl    -12(%rbp), %eax
	leave
	ret

:max2
	movl    %edi, -4(%rbp)
	movl    %esi, -8(%rbp)
	movl    -4(%rbp), %eax
	cmpl    %eax, -8(%rbp)
	cmovge  -8(%rbp), %eax
	leave
	ret

max2 uses much less code due to the usage of instruction cmovge. But the real gain is that max2 does not involve branch jumps, jmp, which would have a significant performance penalty if the predicted result is not right.
So why does a conditional move perform better?
In a typical x86 processor, the execution of an instruction is divided into several stages. Roughly, we have different hardware to deal with different stages. So we do not have to wait for one instruction to finish to start a new one. This is called pipelining.
In a branch case, the following instruction is determined by the preceding one, so we cannot do pipelining. We have to either wait or predict.
In a conditional move case, the execution conditional move instruction is divided into several stages, but the earlier stages like Fetch and Decode does not depend on the result of the previous instruction; only latter stages need the result. Thus, we wait a fraction of one instruction's execution time. This is why the conditional move version is slower than the branch when prediction is easy.
The book Computer Systems: A Programmer's Perspective, second edition explains this in detail. You can check Section 3.6.6 for Conditional Move Instructions, entire Chapter 4 for Processor Architecture, and Section 5.11.2 for a special treatment for Branch Prediction and Misprediction Penalties.
Sometimes, some modern compilers can optimize our code to assembly with better performance, sometimes some compilers can't (the code in question is using Visual Studio's native compiler). Knowing the performance difference between branch and conditional move when unpredictable can help us write code with better performance when the scenario gets so complex that the compiler can not optimize them automatically.

------------------------------
What is the “-->” operator in C++?
<div class="post-text" itemprop="text">
<p>After reading <a href="http://groups.google.com/group/comp.lang.c++.moderated/msg/33f173780d58dd20" rel="noreferrer">Hidden Features and Dark Corners of C++/STL</a> on <code>comp.lang.c++.moderated</code>, I was completely surprised that the following snippet compiled and worked in both Visual Studio 2008 and G++ 4.4.</p>
<p>Here's the code:</p>
<pre><code>#include &lt;stdio.h&gt;
int main()
{
	int x = 10;
	while (x --&gt; 0) // x goes to 0
	{
		printf("%d ", x);
	}
}
</code></pre>
<p>I'd assume this is C, since it works in GCC as well. Where is this defined in the standard, and where has it come from?</p>
</div>
List of answers:


===>
What is the “-->” operator in C++?

--> is not an operator. It is in fact two separate operators, -- and >.
The conditional's code decrements x, while returning x's original (not decremented) value, and then compares the original value with 0 using the > operator.
To better understand, the statement could be written as follows:
while( (x--) > 0 )


===>
What is the “-->” operator in C++?

Or for something completely different... x slides to 0
while (x --\
			\
			 \
			  \
			   > 0)
	 printf("%d ", x);

Not so mathematical, but... every picture paints a thousand words...

===>
What is the “-->” operator in C++?

That's a very complicated operator, so even ISO/IEC JTC1 (Joint Technical Committee 1) placed its description in two different parts of the C++ Standard.
Joking aside, they are two different operators: -- and > described respectively in §5.2.6/2 and §5.9 of the C++03 Standard.

------------------------------
The Definitive C++ Book Guide and List
<div class="post-text" itemprop="text">
<p>This question attempts to collect the few pearls among the dozens of bad C++ books that are published every year.</p>
<p>Unlike many other programming languages, which are often picked up on the go from tutorials found on the Internet, few are able to quickly pick up C++ without studying a well-written C++ book. It is way too big and complex for doing this. In fact, it is so big and complex, that <strong><em>there are very many very bad C++ books</em></strong> out there. And we are not talking about bad style, but things like sporting <em>glaringly obvious factual errors</em> and <em>promoting abysmally bad programming styles</em>.</p>
<p>Please edit the accepted answer to provide <strong>quality books</strong> and an approximate skill level — <em>preferably</em> <strong>after</strong> <em>discussing your addition in <a href="http://chat.stackoverflow.com/rooms/10/loungec">the C++ chat room</a></em>. (The regulars might mercilessly undo your work if they disagree with a recommendation.) Add a short blurb/description about each book that you have personally read/benefited from. Feel free to debate quality, headings, etc. Books that meet the criteria will be added to the list.  Books that have reviews by the Association of C and C++ Users (ACCU) have links to the review. </p>
<p><sub>*Note: FAQs and other resources can be found in the <a href="https://stackoverflow.com/tags/c%2b%2b/info">C++ tag info</a> and under <a class="post-tag" href="/questions/tagged/c%2b%2b-faq" rel="tag" title="show questions tagged 'c++-faq'">c++-faq</a>. </sub></p>
</div>
List of answers:


===>
The Definitive C++ Book Guide and List

Beginner
Introductory, no previous programming experience

C++ Primer * (Stanley Lippman, Josée Lajoie, and Barbara E. Moo)  (updated for C++11) Coming at 1k pages, this is a very thorough introduction into C++ that covers just about everything in the language in a very accessible format and in great detail. The fifth edition (released August 16, 2012) covers C++11. [Review]
Programming: Principles and Practice Using C++ (Bjarne Stroustrup, 2nd Edition - May 25, 2014) (updated for C++11/C++14) An introduction to programming using C++ by the creator of the language. A good read, that assumes no previous programming experience, but is not only for beginners.


* Not to be confused with C++ Primer Plus (Stephen Prata), with a significantly less favorable review.

Introductory, with previous programming experience

A Tour of C++ (Bjarne Stroustrup) (2nd edition  for C++17) The “tour” is a quick (about 180 pages and 14 chapters) tutorial overview of all of standard C++ (language and standard library, and using C++11) at a moderately high level for people who already know C++ or at least are experienced programmers. This book is an extended version of the material that constitutes Chapters 2-5 of The C++ Programming Language, 4th edition.
Accelerated C++ (Andrew Koenig and Barbara Moo, 1st Edition - August 24, 2000)  This basically covers the same ground as the C++ Primer, but does so on a fourth of its space. This is largely because it does not attempt to be an introduction to programming, but an introduction to C++ for people who've previously programmed in some other language. It has a steeper learning curve, but, for those who can cope with this, it is a very compact introduction to the language. (Historically, it broke new ground by being the first beginner's book to use a modern approach to teaching the language.) Despite this, the C++
it teaches is purely C++98. [Review]

Best practices

Effective C++ (Scott Meyers, 3rd Edition - May 22, 2005)  This was written with the aim of being the best second book C++ programmers should read, and it succeeded. Earlier editions were aimed at programmers coming from C, the third edition changes this and targets programmers coming from languages like Java. It presents ~50 easy-to-remember rules of thumb along with their rationale in a very accessible (and enjoyable) style. For C++11 and C++14 the examples and a few issues are outdated and Effective Modern C++ should be preferred. [Review]
Effective Modern C++ (Scott Meyers) This is basically the new version of Effective C++, aimed at C++ programmers making the transition from C++03 to C++11 and C++14.
Effective STL (Scott Meyers)  This aims to do the same to the part of the standard library coming from the STL what Effective C++ did to the language as a whole: It presents rules of thumb along with their rationale. [Review]


Intermediate

More Effective C++ (Scott Meyers) Even more rules of thumb than Effective C++. Not as important as the ones in the first book, but still good to know.
Exceptional C++ (Herb Sutter)  Presented as a set of puzzles, this has one of the best and thorough discussions of the proper resource management and exception safety in C++ through Resource Acquisition is Initialization (RAII) in addition to in-depth coverage of a variety of other topics including the pimpl idiom, name lookup, good class design, and the C++ memory model. [Review]
More Exceptional C++ (Herb Sutter)  Covers additional exception safety topics not covered in Exceptional C++, in addition to discussion of effective object-oriented programming in C++ and correct use of the STL. [Review]
Exceptional C++ Style (Herb Sutter)  Discusses generic programming, optimization, and resource management; this book also has an excellent exposition of how to write modular code in C++ by using non-member functions and the single responsibility principle. [Review]
C++ Coding Standards (Herb Sutter and Andrei Alexandrescu) “Coding standards” here doesn't mean “how many spaces should I indent my code?”  This book contains 101 best practices, idioms, and common pitfalls that can help you to write correct, understandable, and efficient C++ code. [Review]
C++ Templates: The Complete Guide (David Vandevoorde and Nicolai M. Josuttis) This is the book about templates as they existed before C++11.  It covers everything from the very basics to some of the most advanced template metaprogramming and explains every detail of how templates work (both conceptually and at how they are implemented) and discusses many common pitfalls.  Has excellent summaries of the One Definition Rule (ODR) and overload resolution in the appendices. A second edition covering C++11, C++14 and C++17 has been already published . [Review]
C++ 17 - The Complete Guide (Nicolai M. Josuttis) This book describes all the new features introduced in the C++17 Standard covering everything from the simple ones like 'Inline Variables', 'constexpr if' all the way up to 'Polymorphic Memory Resources' and 'New and Delete with overaligned Data'.


Advanced

Modern C++ Design (Andrei Alexandrescu)  A groundbreaking book on advanced generic programming techniques.  Introduces policy-based design, type lists, and fundamental generic programming idioms then explains how many useful design patterns (including small object allocators, functors, factories, visitors, and multi-methods) can be implemented efficiently, modularly, and cleanly using generic programming. [Review]
C++ Template Metaprogramming (David Abrahams and Aleksey Gurtovoy)
C++ Concurrency In Action (Anthony Williams) A book covering C++11 concurrency support including the thread library, the atomics library, the C++ memory model, locks and mutexes, as well as issues of designing and debugging multithreaded applications.
Advanced C++ Metaprogramming (Davide Di Gennaro) A pre-C++11 manual of TMP techniques, focused more on practice than theory.  There are a ton of snippets in this book, some of which are made obsolete by type traits, but the techniques, are nonetheless useful to know.  If you can put up with the quirky formatting/editing, it is easier to read than Alexandrescu, and arguably, more rewarding.  For more experienced developers, there is a good chance that you may pick up something about a dark corner of C++ (a quirk) that usually only comes about through extensive experience.


Reference Style - All Levels

The C++ Programming Language (Bjarne Stroustrup) (updated for C++11) The classic introduction to C++ by its creator. Written to parallel the classic K&R, this indeed reads very much like it and covers just about everything from the core language to the standard library, to programming paradigms to the language's philosophy. [Review] Note: All releases of the C++ standard are tracked in this question: Where do I find the current C++ standard.
C++ Standard Library Tutorial and Reference (Nicolai Josuttis) (updated for C++11) The introduction and reference for the C++ Standard Library. The second edition (released on April 9, 2012) covers C++11. [Review]
The C++ IO Streams and Locales (Angelika Langer and Klaus Kreft)  There's very little to say about this book except that, if you want to know anything about streams and locales, then this is the one place to find definitive answers. [Review]

C++11/14/17/… References:

The C++11/14/17 Standard (INCITS/ISO/IEC 14882:2011/2014/2017) This, of course, is the final arbiter of all that is or isn't C++. Be aware, however, that it is intended purely as a reference for experienced users willing to devote considerable time and effort to its understanding. The C++17 standard is released in electronic form for 198 Swiss Francs.
The C++17 standard is available, but seemingly not in an economical form – directly from the ISO it costs 198 Swiss Francs (about $200 US). For most people, the final draft before standardization is more than adequate (and free). Many will prefer an even newer draft, documenting new features that are likely to be included in C++20.
Overview of the New C++ (C++11/14) (PDF only) (Scott Meyers) (updated for C++14) These are the presentation materials (slides and some lecture notes) of a three-day training course offered by Scott Meyers, who's a highly respected author on C++. Even though the list of items is short, the quality is high.
The C++ Core Guidelines (C++11/14/17/…) (edited by Bjarne Stroustrup and Herb Sutter) is an evolving online document consisting of a set of guidelines for using modern C++ well. The guidelines are focused on relatively higher-level issues, such as interfaces, resource management, memory management and concurrency affecting application architecture and library design. The project was announced at CppCon'15 by Bjarne Stroustrup and others and welcomes contributions from the community. Most guidelines are supplemented with a rationale and examples as well as discussions of possible tool support. Many rules are designed specifically to be automatically checkable by static analysis tools.
The C++ Super-FAQ (Marshall Cline, Bjarne Stroustrup and others) is an effort by the Standard C++ Foundation to unify the C++ FAQs previously maintained individually by Marshall Cline and Bjarne Stroustrup and also incorporating new contributions. The items mostly address issues at an intermediate level and are often written with a humorous tone. Not all items might be fully up to date with the latest edition of the C++ standard yet.
cppreference.com (C++03/11/14/17/…) (initiated by Nate Kohl) is a wiki that summarizes the basic core-language features and has extensive documentation of the C++ standard library. The documentation is very precise but is easier to read than the official standard document and provides better navigation due to its wiki nature. The project documents all versions of the C++ standard and the site allows filtering the display for a specific version. The project was presented by Nate Kohl at CppCon'14.


Classics / Older
Note: Some information contained within these books may not be up-to-date or no longer considered best practice.

The Design and Evolution of C++ (Bjarne Stroustrup)  If you want to know why the language is the way it is, this book is where you find answers. This covers everything before the standardization of C++.
Ruminations on C++ - (Andrew Koenig and Barbara Moo) [Review]
Advanced C++ Programming Styles and Idioms (James Coplien)  A predecessor of the pattern movement, it describes many C++-specific “idioms”. It's certainly a very good book and might still be worth a read if you can spare the time, but quite old and not up-to-date with current C++.
Large Scale C++ Software Design (John Lakos)  Lakos explains techniques to manage very big C++ software projects. Certainly, a good read, if it only was up to date. It was written long before C++ 98 and misses on many features (e.g. namespaces) important for large-scale projects. If you need to work in a big C++ software project, you might want to read it, although you need to take more than a grain of salt with it. The first volume of a new edition is expected in 2018.
Inside the C++ Object Model (Stanley Lippman)  If you want to know how virtual member functions are commonly implemented and how base objects are commonly laid out in memory in a multi-inheritance scenario, and how all this affects performance, this is where you will find thorough discussions of such topics.
The Annotated C++ Reference Manual (Bjarne Stroustrup, Margaret A. Ellis) This book is quite outdated in the fact that it explores the 1989 C++ 2.0 version - Templates, exceptions, namespaces and new casts were not yet introduced. Saying that however, this book goes through the entire C++ standard of the time explaining the rationale, the possible implementations, and features of the language. This is not a book to learn programming principles and patterns on C++, but to understand every aspect of the C++ language.
Thinking in C++ (Bruce Eckel, 2nd Edition, 2000).  Two volumes; is a tutorial style free set of intro level books. Downloads: vol 1, vol 2. Unfortunately they’re marred by a number of trivial errors (e.g. maintaining that temporaries are automatically const), with no official errata list. A partial 3rd party errata list is available at (http://www.computersciencelab.com/Eckel.htm), but it’s apparently not maintained.
Scientific and Engineering C++: An Introduction to Advanced Techniques and Examples (John Barton and Lee Nackman)
It is a comprehensive and very detailed book that tried to explain and make use of all the features available in C++, in the context of numerical methods. It introduced at the time several new techniques, such as the Curiously Recurring Template Pattern (CRTP, also called Barton-Nackman trick).
It pioneered several techniques such as dimensional analysis and automatic differentiation.
It came with a lot of compilable and useful code, ranging from an expression parser to a Lapack wrapper.
The code is still available here: http://www.informit.com/store/scientific-and-engineering-c-plus-plus-an-introduction-9780201533934.
Unfortunately, the books have become somewhat outdated in the style and C++ features, however, it was an incredible tour-de-force at the time (1994, pre-STL).
The chapters on dynamics inheritance are a bit complicated to understand and not very useful.
An updated version of this classic book that includes move semantics and the lessons learned from the STL would be very nice.


------------------------------
What are the differences between a pointer variable and a reference variable in C++?
<div class="post-text" itemprop="text">
<p>I know references are syntactic sugar, so code is easier to read and write.</p>
<p>But what are the differences?</p>
<hr/>
<p>Summary from answers and links below:</p>
<ol>
<li>A pointer can be re-assigned any number of times while a reference cannot be re-assigned after binding.</li>
<li>Pointers can point nowhere (<code>NULL</code>), whereas a reference always refers to an object.</li>
<li>You can't take the address of a reference like you can with pointers.</li>
<li>There's no "reference arithmetic" (but you can take the address of an object pointed by a reference and do pointer arithmetic on it as in <code>&amp;obj + 5</code>).</li>
</ol>
<p>To clarify a misconception:</p>
<blockquote>
<p><em>The C++ standard is very careful to avoid dictating how a compiler may
  implement references, but every C++ compiler implements
  references as pointers. That is, a declaration such as:</em></p>
<pre><code>int &amp;ri = i;
</code></pre>
<p><strong><em>if it's not optimized away entirely</em></strong>, <em>allocates the same amount of storage
  as a pointer, and places the address
  of <code>i</code> into that storage.</em></p>
</blockquote>
<p><strong><em>So, a pointer and a reference both use the same amount of memory.</em></strong></p>
<p>As a general rule,</p>
<ul>
<li>Use references in function parameters and return types to provide useful and self-documenting interfaces.</li>
<li>Use pointers for implementing algorithms and data structures.</li>
</ul>
<p>Interesting read:</p>
<ul>
<li>My all-time favorite <a href="http://yosefk.com/c++fqa/ref.html" rel="noreferrer">C++ FAQ lite</a>.</li>
<li><a href="http://www.embedded.com/electronics-blogs/programming-pointers/4023307/References-vs-Pointers" rel="noreferrer">References vs. Pointers</a>.</li>
<li><a href="http://www.embedded.com/electronics-blogs/programming-pointers/4024641/An-Introduction-to-References" rel="noreferrer">An Introduction to References</a>.</li>
<li><a href="http://www.embedded.com/electronics-blogs/programming-pointers/4023290/References-and-const" rel="noreferrer">References and const</a>.</li>
</ul>
</div>
List of answers:


===>
What are the differences between a pointer variable and a reference variable in C++?


A pointer can be re-assigned:
int x = 5;
int y = 6;
int *p;
p =  &x;
p = &y;
*p = 10;
assert(x == 5);
assert(y == 10);

A reference cannot, and must be assigned at initialization:
int x = 5;
int y = 6;
int &r = x;

A pointer has its own memory address and size on the stack (4 bytes on x86), whereas a reference shares the same memory address (with the original variable) but also takes up some space on the stack.  Since a reference has the same address as the original variable itself, it is safe to think of a reference as another name for the same variable.  Note: What a pointer points to can be on the stack or heap.  Ditto a reference. My claim in this statement is not that a pointer must point to the stack.  A pointer is just a variable that holds a memory address.  This variable is on the stack.  Since a reference has its own space on the stack, and since the address is the same as the variable it references.  More on stack vs heap.  This implies that there is a real address of a reference that the compiler will not tell you.
int x = 0;
int &r = x;
int *p = &x;
int *p2 = &r;
assert(p == p2);

You can have pointers to pointers to pointers offering extra levels of indirection.  Whereas references only offer one level of indirection.
int x = 0;
int y = 0;
int *p = &x;
int *q = &y;
int **pp = &p;
pp = &q;//*pp = q
**pp = 4;
assert(y == 4);
assert(x == 0);

Pointer can be assigned nullptr directly, whereas reference cannot. If you try hard enough, and you know how, you can make the address of a reference nullptr.  Likewise, if you try hard enough you can have a reference to a pointer, and then that reference can contain nullptr.
int *p = nullptr;
int &r = nullptr; <--- compiling error
int &r = *p;  <--- likely no compiling error, especially if the nullptr is hidden behind a function call, yet it refers to a non-existent int at address 0

Pointers can iterate over an array, you can use ++ to go to the next item that a pointer is pointing to, and + 4 to go to the 5th element.  This is no matter what size the object is that the pointer points to.
A pointer needs to be dereferenced with * to access the memory location it points to, whereas a reference can be used directly.  A pointer to a class/struct uses -> to access it's members whereas a reference uses a ..
A pointer is a variable that holds a memory address.  Regardless of how a reference is implemented, a reference has the same memory address as the item it references.
References cannot be stuffed into an array, whereas pointers can be (Mentioned by user @litb)
Const references can be bound to temporaries. Pointers cannot (not without some indirection):
const int &x = int(12); //legal C++
int *y = &int(12); //illegal to dereference a temporary.

This makes const& safer for use in argument lists and so forth.


===>
What are the differences between a pointer variable and a reference variable in C++?

What's a C++ reference (for C programmers)
A reference can be thought of as a constant pointer (not to be confused with a pointer to a constant value!) with automatic indirection, ie the compiler will apply the * operator for you.
All references must be initialized with a non-null value or compilation will fail. It's neither possible to get the address of a reference - the address operator will return the address of the referenced value instead - nor is it possible to do arithmetics on references.
C programmers might dislike C++ references as it will no longer be obvious when indirection happens or if an argument gets passed by value or by pointer without looking at function signatures.
C++ programmers might dislike using pointers as they are considered unsafe - although references aren't really any safer than constant pointers except in the most trivial cases - lack the convenience of automatic indirection and carry a different semantic connotation.
Consider the following statement from the C++ FAQ:

Even though a reference is often implemented using an address in the
  underlying assembly language, please do not think of a reference as a
  funny looking pointer to an object. A reference is the object. It is
  not a pointer to the object, nor a copy of the object. It is the
  object.

But if a reference really were the object, how could there be dangling references? In unmanaged languages, it's impossible for references to be any 'safer' than pointers - there generally just isn't a way to reliably alias values across scope boundaries!
Why I consider C++ references useful
Coming from a C background, C++ references may look like a somewhat silly concept, but one should still use them instead of pointers where possible: Automatic indirection is convenient, and references become especially useful when dealing with RAII - but not because of any perceived safety advantage, but rather because they make writing idiomatic code less awkward.
RAII is one of the central concepts of C++, but it interacts non-trivially with copying semantics. Passing objects by reference avoids these issues as no copying is involved. If references were not present in the language, you'd have to use pointers instead, which are more cumbersome to use, thus violating the language design principle that the best-practice solution should be easier than the alternatives.

===>
What are the differences between a pointer variable and a reference variable in C++?

If you want to be really pedantic, there is one thing you can do with a reference that you can't do with a pointer: extend the lifetime of a temporary object. In C++ if you bind a const reference to a temporary object, the lifetime of that object becomes the lifetime of the reference.
std::string s1 = "123";
std::string s2 = "456";

std::string s3_copy = s1 + s2;
const std::string& s3_reference = s1 + s2;

In this example s3_copy copies the temporary object that is a result of the concatenation. Whereas s3_reference in essence becomes the temporary object. It's really a reference to a temporary object that now has the same lifetime as the reference.
If you try this without the const it should fail to compile. You cannot bind a non-const reference to a temporary object, nor can you take its address for that matter.

------------------------------
How do I iterate over the words of a string?
<div class="post-text" itemprop="text">
<p>I'm trying to iterate over the words of a string.</p>
<p>The string can be assumed to be composed of words separated by whitespace.</p>
<p>Note that I'm not interested in C string functions or that kind of character manipulation/access. Also, please give precedence to elegance over efficiency in your answer.</p>
<p>The best solution I have right now is:</p>
<pre><code>#include &lt;iostream&gt;
#include &lt;sstream&gt;
#include &lt;string&gt;

using namespace std;

int main()
{
	string s = "Somewhere down the road";
	istringstream iss(s);

	do
	{
		string subs;
		iss &gt;&gt; subs;
		cout &lt;&lt; "Substring: " &lt;&lt; subs &lt;&lt; endl;
	} while (iss);
}
</code></pre>
<p>Is there a more elegant way to do this?</p>
</div>
List of answers:


===>
How do I iterate over the words of a string?

For what it's worth, here's another way to extract tokens from an input string, relying only on standard library facilities. It's an example of the power and elegance behind the design of the STL.
#include <iostream>
#include <string>
#include <sstream>
#include <algorithm>
#include <iterator>

int main() {
	using namespace std;
	string sentence = "And I feel fine...";
	istringstream iss(sentence);
	copy(istream_iterator<string>(iss),
		 istream_iterator<string>(),
		 ostream_iterator<string>(cout, "\n"));
}

Instead of copying the extracted tokens to an output stream, one could insert them into a container, using the same generic copy algorithm.
vector<string> tokens;
copy(istream_iterator<string>(iss),
	 istream_iterator<string>(),
	 back_inserter(tokens));

... or create the vector directly:
vector<string> tokens{istream_iterator<string>{iss},
					  istream_iterator<string>{}};


===>
How do I iterate over the words of a string?

I use this to split string by a delimiter. The first puts the results in a pre-constructed vector, the second returns a new vector.
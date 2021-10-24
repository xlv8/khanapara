
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
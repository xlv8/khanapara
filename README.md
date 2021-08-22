
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
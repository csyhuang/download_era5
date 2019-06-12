import concurrent.futures as cf
import tqdm


def parallel_process(array, function, n_jobs, use_kwargs=False,
                     extra_kwargs={}):
    """
        Modified from http://danshiebler.com/2016-09-14-parallel-progress-bar/
        A parallel version of the map function with a progress bar.

        Args:
            array(array-like): An array to iterate over.
            function(function): A python function to apply to the elements
            of array
            n_jobs(int, default=16): The number of cores to use
            use_kwargs(boolean, default=False): Whether to consider the
            elements of array as dictionaries of keyword arguments to function
        Returns:
            [function(array[0]), function(array[1]), ...]
    """
    # If we set n_jobs to 1, just run a list comprehension. This is useful for
    # benchmarking and debugging.
    if n_jobs == 1:
        out = [function(**a, **extra_kwargs) if use_kwargs
               else function(a, **extra_kwargs) for a in tqdm(array)]
    else:
        # Assemble the workers
        pool = cf.ProcessPoolExecutor(max_workers=n_jobs)
        # Pass the elements of array into function
        if use_kwargs:
            futures = [pool.submit(function, **a, **extra_kwargs)
                       for a in array]
        else:
            futures = [pool.submit(function, a, **extra_kwargs)
                       for a in array]
        kwargs = {
            'total': len(futures),
            'unit': 'it',
            'unit_scale': True,
            'leave': True
        }
        # Print out the progress as tasks complete
        for f in tqdm(cf.as_completed(futures), **kwargs):
            pass
        pool.shutdown(wait=True)

        out = []
        # Get the results from the futures.
        for i, future in tqdm(enumerate(futures)):
            try:
                out.append(future.result())
            except Exception as e:
                out.append(e)
    return(out)

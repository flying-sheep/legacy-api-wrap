from functools import wraps
from inspect import signature, Parameter

def legacy_api(*positionals):
	def wrapper(fn):
		sig = signature(fn)
		par_types = {p.kind for p in sig.parameters}
		n_positional = None if Parameter.s
		
		@wraps(fn)
		def fn_compatible(*args, **kw):
			if len(args) > len(fn)
			
			return fn_compatible(*args, **kw)
		return fn_new
	return wrapper


def old(a, b=None, d=1, c=2):
	pass


@legacy_api('d', 'c')
def new(a, b=None, *, c=2, d=1, e=3):
	return dict(a=a, b=b, c=c, d=d, e=e)


# Tests ---------------------------


def test_inspection_correct():
	assert str(signature(new)) == '(a, b=None, *, c=2, d=1, e=3)'


def test_new_param_available():
	new(12, e=13)


def test_old_positional_order():
	from pytest import warns
	with warns(DeprecationWarning):
		res = new(12, 13, 14)
	assert res['d'] == 14


if __name__ == '__main__':
	from pytest import main
	import sys
	main(sys.argv)  # call on current file

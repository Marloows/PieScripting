
function [x_e, x] = newtons_method(f, df, x_0, I, delta_x)

	if ~exist('f', 'var')
		f = @(x) x^3 + x^2 + x + 1;
	end

	if ~exist('df', 'var')
		df = @(x) 3*x^2 + 2*x + 1;
	end

	if ~exist('x_0', 'var')
		x_0 = 0;
	end

	if ~exist('I', 'var')
		I = 1e2;
	end

	if ~exist('delta_x', 'var')
		delta_x = 1e-6;
	end

	x = x_0;

	x(I) = 0;

	i = 1;

	while i <= I
		x(i+1) = x(i) - f(x(i))/df(x(i));
		i = i + 1;
		if abs(x(i) - x(i-1)) < delta_x
			x = x(1:i);
			break
		end
	end

	x_e = x(end);

end


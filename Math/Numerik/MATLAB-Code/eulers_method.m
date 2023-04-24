
function  varargout = eulers_method(dY, Y0, dt, tRange)

	if ~exist('dY', 'var')
		dY = @(t, y, dy) (2*dy -5*y-5/2*t + 1/2 );
	end

	if ~exist('Y0', 'var')
		Y0 = [1 1];
	end

	if ~exist('dt', 'var')
		dt = 1e-2;
	end

	if ~exist('tRange', 'var')
		tRange(2) = 10;
	end

	dY = diff_func_vec(dY, length(Y0));

	Y0 = reshape(Y0, 1, length(Y0));

	Y = solve_ode(dY, Y0, dt, tRange);

	nOutputs = nargout;

	varargout = cell(1,nOutputs);

	if nOutputs < 2
		varargout{1} = Y(:, 2);
		varargout = varargout(1);
		return
	end

	for k = 1:nOutputs
		varargout{k} = Y(:, k);
	end

end

function dY = diff_func_vec(f_x, n)
	dY = repmat({@quo_approx}, 1, n);
	dY{end+1} = f_x;
end



function y_n = quo_approx(y, dy, dx)
	y_n = y + dy*dx;
end


function Y = solve_ode(dY, Y0, dt, tRange)

	Y = tRange(1):dt:tRange(2);

	Y = Y';

	E = length(Y0);     %just to fit everything neatly

	Y(end, E + 2) = 0;

	Y(1, 2:end-1) = Y0;
	t = Y(1, 1:end-1);    
	t = num2cell(t);
	f = dY{end};
	t = f(t{:});
	Y(1, end) = t;

	i = 2;

	[R, ~] = size(Y);

	while i <= R
		index = 1;
		while index <= E
			Y(i, index + 1) = dY{index}(Y(i-1, index + 1), Y(i-1, index + 2), dt);
			index = index + 1;
		end
		t = num2cell(Y(i, 1:end-1));
		Y(i, end) = dY{end}(t{:});
		Y(i, 1) = Y(i-1, 1) + dt;
		i = i + 1;
	end
end


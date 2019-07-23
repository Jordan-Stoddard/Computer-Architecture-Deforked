$_$wp(1);
const $_$wvd1 = $_$w(1, 0), getStored = function () {
        $_$wf(1);
        let value = ($_$w(1, 1), undefined);
        const $_$wvd3 = $_$w(1, 2), innerFunction = inner => {
                $_$wf(1);
                if ($_$w(1, 3), inner === undefined) {
                    return $_$w(1, 4), value;
                } else {
                    let oldValue = ($_$w(1, 5), value);
                    $_$w(1, 6), value = inner;
                    return $_$w(1, 7), oldValue;
                }
            };
        return $_$w(1, 8), innerFunction;
    };
const a = ($_$w(1, 9), getStored());
let v = ($_$w(1, 10), 10);
$_$w(1, 11), $_$tracer.log(a(), 'a()', 1, 11);
$_$w(1, 12), $_$tracer.log(a(v), 'a(v)', 1, 12);
$_$w(1, 13), $_$tracer.log(a(), 'a()', 1, 13);
$_$w(1, 14), $_$tracer.log(a(), 'a()', 1, 14);
$_$w(1, 15), $_$tracer.log(a(), 'a()', 1, 15);
$_$wpe(1);
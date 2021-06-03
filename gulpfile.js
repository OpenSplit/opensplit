const { watch, series, parallel, task } = require('gulp');
const { script, sass, copy, pug, clean } = require('codemonauts-gulp-tasks');

const tailwindcss = require('tailwindcss');


task('sass', function () {
    extras = [tailwindcss('./tailwind.config.js')]
    return sass(['src/sass/*.sass'], 'src/sass/', 'opensplit/static/css', extras);
});

task('clean', function () {
    return clean([
        'opensplit/static/css/**/*',
    ]);
});


task('watch', function () {
    watch(['src/sass/*'], series('sass'));
});


task('build', series('clean', parallel('sass')));

task('default', series('clean', 'build', 'watch'));

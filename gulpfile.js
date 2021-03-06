const { watch, series, parallel, task } = require('gulp');
const { script, sass, copy, pug, clean } = require('codemonauts-gulp-tasks');

const tailwindcss = require('tailwindcss');


task('sass', function () {
    extras = [tailwindcss('./tailwind.config.js')]
    return sass(['src/sass/*.sass'], 'src/sass/', 'opensplit/static/css', extras);
});

task('js', function () {
    return script('src/js/script.js', 'opensplit/static/js')
})

task('img', function () {
    return copy('src/img/*', 'opensplit/static/img')
})

task('clean', function () {
    return clean([
        'opensplit/static/css/**/*',
    ]);
});


task('watch', function () {
    watch(['src/sass/*', 'tailwind.config.js'], series('sass'));
    watch(['src/js/*'], series('js'));
    watch(['src/img/*'], series('img'));
});


task('build', series('clean', parallel('sass', 'js', 'img')));

task('default', series('clean', 'build', 'watch'));

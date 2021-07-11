---
title: F2PY
---

Just a collection of attributes that describes an extension
    module and everything needed to build it (hopefully in a portable
    way, but there are hooks that let you be as unportable as you need).

    Instance attributes:
      name : string
        the full name of the extension, including any packages -- ie.
        *not* a filename or pathname, but Python dotted name
      sources : [string]
        list of source filenames, relative to the distribution root
        (where the setup script lives), in Unix form (slash-separated)
        for portability.  Source files may be C, C++, SWIG (.i),
        platform-specific resource files, or whatever else is recognized
        by the "build_ext" command as source for a Python extension.
      include_dirs : [string]
        list of directories to search for C/C++ header files (in Unix
        form for portability)
      define_macros : [(name : string, value : string|None)]
        list of macros to define; each macro is defined using a 2-tuple,
        where 'value' is either the string to define it to or None to
        define it without a particular value (equivalent of "#define
        FOO" in source or -DFOO on Unix C compiler command line)
      undef_macros : [string]
        list of macros to undefine explicitly
      library_dirs : [string]
        list of directories to search for C/C++ libraries at link time
      libraries : [string]
        list of library names (not filenames or paths) to link against
      runtime_library_dirs : [string]
        list of directories to search for C/C++ libraries at run time
        (for shared extensions, this is when the extension is loaded)
      extra_objects : [string]
        list of extra files to link with (eg. object files not implied
        by 'sources', static library that must be explicitly specified,
        binary resource files, etc.)
      extra_compile_args : [string]
        any extra platform- and compiler-specific information to use
        when compiling the source files in 'sources'.  For platforms and
        compilers where "command line" makes sense, this is typically a
        list of command-line arguments, but for other platforms it could
        be anything.
      extra_link_args : [string]
        any extra platform- and compiler-specific information to use
        when linking object files together to create the extension (or
        to create a new static Python interpreter).  Similar
        interpretation as for 'extra_compile_args'.
      export_symbols : [string]
        list of symbols to be exported from a shared extension.  Not
        used on all platforms, and not generally necessary for Python
        extensions, which typically export exactly one symbol: "init" +
        extension_name.
      swig_opts : [string]
        any extra options to pass to SWIG if a source file has the .i
        extension.
      depends : [string]
        list of files that the extension depends on
      language : string
        extension language (i.e. "c", "c++", "objc"). Will be detected
        from the source extensions if not provided.
      optional : boolean
        specifies that a build failure in the extension should not abort the
        build process, but simply not install the failing extension.

拡張モジュールとそれを構築するために必要なすべてのものを説明する属性の集まりです。
    モジュールと、それを構築するために必要なすべてのものを記述した属性の集まりです（できれば移植可能な方法で
    しかし、必要に応じて移植不可能にするためのフックがあります）。)

    インスタンスの属性
      name : 文字列
        パッケージを含めた拡張モジュールのフルネーム。
        *つまり、ファイル名やパス名ではなく、Pythonのドット付きの名前です。
      source : [文字列]...
        ディストリビューションルート(セットアップスクリプトが置かれている場所)からの相対的なソースファイル名のリストです。
        ディストリビューションのルート（セットアップスクリプトが置かれている場所）からの相対的なソースファイル名のリストで、Unix形式（スラッシュで区切られています）。
        移植性のためです。 ソースファイルは、C、C++、SWIG (.i),
        プラットフォーム固有のリソースファイルなど、「build_ext」コマンドで
        build_ext" コマンドで Python 拡張機能のソースとして認識されるものであれば何でも構いません。
      include_dirs : [文字列].
        C/C++ヘッダーファイルを検索するディレクトリのリスト (移植性を考慮してUnix形式で)
        形式で移植可能)
      define_macros : [(name : string, value : string|None)] 定義するマクロのリスト。
        定義するマクロのリスト。各マクロは2-タプルで定義されます。
        各マクロは2つのタプルで定義され、'value'は定義する文字列か、特定の値を持たないNone
        特定の値を指定せずに定義します（ソースの「#define
        FOO "に相当し、Unix Cコンパイラのコマンドラインでは-DFOOとなります。)
      undef_macros : [文字列].
        明示的に定義を解除するマクロのリスト
      library_dirs : [文字列]
        リンク時にC/C++ライブラリを検索するディレクトリのリスト
      ライブラリ : [文字列]
        リンクするライブラリ名（ファイル名やパスではない）のリスト
      ランタイム_ライブラリ_dirs : [文字列]
        実行時にC/C++ライブラリを検索するディレクトリのリスト
        共有されている拡張機能の場合は、拡張機能がロードされたときに検索されます）。
      extra_objects : [文字列]リンクする追加ファイルのリスト
        リンクする追加ファイルのリスト（例："sources "に含まれないオブジェクトファイル
        リンクする追加ファイルのリスト（例：'sources'で暗示されていないオブジェクトファイル、明示的に指定しなければならないスタティックライブラリ。
        バイナリリソースファイルなど）。)
      extra_compile_args : [文字列].
        'sources'のソースファイルをコンパイルする際に使用する、プラットフォームやコンパイラに固有の情報
        プラットフォームおよびコンパイラ固有の情報です。 プラットフォームやコンパイラが
        コンパイラの場合、通常はコマンドライン引数のリストになります。
        コマンドライン引数のリストですが、他のプラットフォームでは何でもかまいません。
        何でもよいのです。
      extra_link_args : [文字列].
        オブジェクトファイルをリンクして拡張子を作成する際に使用する
        エクステンションを作成するためにオブジェクトファイルをリンクする際に使用する
        新しい静的な Python インタープリタを作成するために）オブジェクトファイルをリンクする際に使用する、プラットフォームおよびコンパイラ固有の追加情報です。)  同様の
        extra_compile_args'と同様の解釈です。
      export_symbols : [string] (文字列)
        共有拡張からエクスポートされるシンボルのリストです。 全てのプラットフォームで使用されているわけではありません。
        すべてのプラットフォームで使用されているわけではありません。
        拡張機能では一般的に必要ありません。"init "+。
        extension_name.
      swig_opts : [文字列].
        ソースファイルの拡張子が.iの場合に、SWIGに渡す追加オプション。
        拡張子がついている場合に、SWIGに渡す追加オプションです。
      depends : [string] (依存関係)
        拡張子が依存しているファイルのリスト
      言語 : 文字列
        拡張子の言語 (例: "c", "c++", "objc")。提供されていない場合は、ソース拡張機能から検出されます。
        提供されていない場合は、ソース拡張機能から検出されます。
      optional : boolean
        拡張機能のビルドに失敗した場合、ビルドプロセスを中断せずに
        ビルドプロセスを中止するのではなく、単に失敗した拡張機能をインストールしないことを指定します。

// Based on https://github.com/graphql/graphiql/blob/HEAD/packages/graphiql-plugin-explorer/examples/index.html

var graphQLFetcher = graphQLParams => {
    return fetch('/graphql', {
        method: 'post',
        body: JSON.stringify(graphQLParams),
    }).then(response => response.json());
};
function GraphiQLWithExplorer() {
    var [query, setQuery] = React.useState(
      '',
    );
    var explorerPlugin = GraphiQLPluginExplorer.useExplorerPlugin({
      query: query,
      onEdit: setQuery,
    });
    return React.createElement(GraphiQL, {
      fetcher: graphQLFetcher,
      defaultEditorToolsVisibility: true,
      plugins: [explorerPlugin],
      query: query,
      onEditQuery: setQuery,
    });
  }
ReactDOM.render(
    React.createElement(GraphiQLWithExplorer),
    document.getElementById('graphiql')
);

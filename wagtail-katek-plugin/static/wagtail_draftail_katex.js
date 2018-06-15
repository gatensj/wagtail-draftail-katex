(() => {

	/*
	This instantiates the React component as window.react
	*/
	const $ = global.jQuery;
	const React = window.React;
	const AtomicBlockUtils = window.DraftJS.AtomicBlockUtils;
	const EditorState = window.DraftJS.EditorState;
	const SelectionState = window.DraftJS.SelectionState;
	const Modifier = window.DraftJS.Modifier;
	const katex = window.katex;

	/*
	A React component that renders nothing.
	We actually create the entities directly in the componentDidMount lifecycle hook.
	This is used for new katex.
	*/
	class KaTeXSource extends React.Component {

		// This fires a windows prompt for new katex.  The else hanles if the user clicks cancel.
		fireWindowsPrompt(entity, katextEquation = 'c = pmsqrt{a^2 + b^2}', ){

			const editorState = this.props['editorState'];
			const entityType = this.props['entityType'];
			const onComplete = this.props['onComplete'];
			const content = editorState.getCurrentContent();

			var text = window.prompt('KaTeX text:', katextEquation);

			if (typeof(text) != 'undefined' && text != null) {

				const contentWithEntity = content.createEntity(
					entityType.type,
					'MUTABLE',
					{
						text: text,
					},
				);

				const entityKey = contentWithEntity.getLastCreatedEntityKey();

				const nextState = AtomicBlockUtils.insertAtomicBlock(
					editorState,
					entityKey,
					' ',
				);

				onComplete(nextState);
			}
			else {
				onComplete(null);
			}

		}

		// The componentDidMount is a draftail event, which allows us to call the previous function fireWindowPrompt.
		componentDidMount() {
			this.fireWindowsPrompt(null);
		}

		// 	This renders nothing, because we create the entities directly in the componentDidMount lifecycle hook.
		render() {
			return null;
		}
	}


	/*
	A React component that renders nothing. We actually create the entities directly in the componentDidMount lifecycle.
	*/
	class KaTeXBlock extends React.Component {

		// This fires the update windows prompt.
		fireUpdateWindowsPrompt() {
			const block = this.props['block'];
			const blockProps = this.props['blockProps'];
			const entityKey = blockProps['entityKey'];
			const editorState = blockProps['editorState'];
			const onRemoveEntity = blockProps['onRemoveEntity'];
			const onEditEntity = blockProps['onEditEntity'];
			const entity = blockProps['entity'];
			const katextEquation = entity.getData()['text'];

			var text = window.prompt('KaTeX text:', katextEquation);

			if (typeof(text) != 'undefined' && text != null) {
				this.updateBlockEntity(editorState, block, {text: text});
			}

		}

		// This updates a block's data in the WYSIWYG editor.
		updateBlockEntity(editorState, block, data){
			const content = editorState.getCurrentContent();
			let nextContent = content.mergeEntityData(block.getEntityAt(0), data);
			nextContent = Modifier.mergeBlockData(
				nextContent,
				new SelectionState({
					anchorKey: block.getKey(),
					anchorOffset: 0,
					focusKey: block.getKey(),
					focusOffset: block.getLength(),
				}),
				{},
			);
			return EditorState.push(editorState, nextContent, 'apply-entity');
		}

		// This renders the katex block. Also fire the function fireUpdateWindowsPrompt when katex block is clicked.
		render() {
			const blockProps = this.props['blockProps'];
			const entity = blockProps['entity'];
			const text = entity.getData()['text'];

			return React.createElement(
				'div',
				{
					role: 'button',
					title: text,
					onMouseDown: () => {
						this.fireUpdateWindowsPrompt();
					},
					dangerouslySetInnerHTML: {
						__html: katex.renderToString(text),
					}
				},
			);

		}

	}

	/*
	This registers the Katex plugin. The Source is for creating new KaTex.  The block is to display the Katex in editor.
	*/
	window.draftail.registerPlugin({
		type: 'KATEX',
		source: KaTeXSource,
		block: KaTeXBlock,
	});


})

();


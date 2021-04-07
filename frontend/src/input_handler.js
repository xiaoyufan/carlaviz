import React, { PureComponent } from "react";
import Websocket from "react-websocket";

const WEBSOCKET_URL = "ws://localhost:13254";

class InputHandler extends PureComponent {
    componentDidMount() {
        this._registerKeyEvents();
    }

    _registerKeyEvents = () => {
        console.debug("registering key events");
        document.addEventListener("keydown", this._handleKeyDown);
    }

    _handleKeyDown = event => {
        console.debug(`Key pressed: ${event.key}`);
        this._handleOutMessage(event.key);
    }

    _handleOpen() {
        console.info(`connected to ${WEBSOCKET_URL}`);
    }

    _handleClose() {
        console.info(`disconnected with ${WEBSOCKET_URL}`);
    }

    _handleInMessage = message => {
        console.debug(`received message: ${message}`);
    }

    _handleOutMessage = message => {
        console.debug(`sending message: ${message}`);
        this.refWebSocket.sendMessage(message);
    }

    render() {
        return (
            <Websocket url={WEBSOCKET_URL}
                onMessage={this._handleInMessage}
                onOpen={this._handleOpen}
                onClose={this._handleClose}
                reconnect={true}
                debug={true}
                ref={Websocket => {
                    this.refWebSocket = Websocket;
                }}
            />
        )
    }
}

export { InputHandler };
import { Fragment, useState } from 'react'
import {
    FolderIcon,
    ServerIcon,
    SignalIcon,
    XMarkIcon,

} from '@heroicons/react/24/outline'
import { Dialog, Transition } from '@headlessui/react'

import { BriefcaseIcon, DocumentIcon } from '@heroicons/react/20/solid'
import Applications from './Applications'
import Sidebar from './Sidebar'
import SortDropdown from '../custom/SortDropdown'


const navigation = [
    { name: 'Applications', href: '#', icon: BriefcaseIcon, current: true },
    { name: 'Resume', href: '#', icon: DocumentIcon, current: false },
    { name: 'Other files', href: '#', icon: FolderIcon, current: false },
]
const teams = [
    { id: 1, name: 'Planetaria', href: '#', initial: 'P', current: false },
    { id: 2, name: 'Protocol', href: '#', initial: 'P', current: false },
    { id: 3, name: 'Tailwind Labs', href: '#', initial: 'T', current: false },
]

const applications = [
    {
        id: 1,
        href: '#',
        company: 'Microsoft',
        role: 'Software Engineer Intern',
        statusText: 'Applied 1m 32s ago',
        notes: 'Deploys from GitHub',
        status: 'offer',
    },
    {
        id: 2,
        href: '#',
        company: 'Microsoft',
        role: 'Software Engineer Intern',
        statusText: 'Applied 1m 32s ago',
        notes: 'Next interview on Monday God willing!',
        status: 'interview',
    },
]


const sortOptions = ["Company Name", "Date Added", "Status"]

const UserHome = () => {
    const [sidebarOpen, setSidebarOpen] = useState(false)

    return (
        <>
            <div>
                <Transition.Root show={sidebarOpen} as={Fragment}>
                    <Dialog as="div" className="relative z-50 xl:hidden" onClose={setSidebarOpen}>
                        <Transition.Child
                            as={Fragment}
                            enter="transition-opacity ease-linear duration-300"
                            enterFrom="opacity-0"
                            enterTo="opacity-100"
                            leave="transition-opacity ease-linear duration-300"
                            leaveFrom="opacity-100"
                            leaveTo="opacity-0"
                        >
                            <div className="fixed inset-0 bg-gray-900/80" />
                        </Transition.Child>

                        <div className="fixed inset-0 flex">
                            <Transition.Child
                                as={Fragment}
                                enter="transition ease-in-out duration-300 transform"
                                enterFrom="-translate-x-full"
                                enterTo="translate-x-0"
                                leave="transition ease-in-out duration-300 transform"
                                leaveFrom="translate-x-0"
                                leaveTo="-translate-x-full"
                            >
                                <Dialog.Panel className="relative mr-16 flex w-full max-w-xs flex-1">
                                    <Transition.Child
                                        as={Fragment}
                                        enter="ease-in-out duration-300"
                                        enterFrom="opacity-0"
                                        enterTo="opacity-100"
                                        leave="ease-in-out duration-300"
                                        leaveFrom="opacity-100"
                                        leaveTo="opacity-0"
                                    >
                                        <div className="absolute left-full top-0 flex w-16 justify-center pt-5">
                                            <button type="button" className="-m-2.5 p-2.5" onClick={() => setSidebarOpen(false)}>
                                                <span className="sr-only">Close sidebar</span>
                                                <XMarkIcon className="h-6 w-6 text-white" aria-hidden="true" />
                                            </button>
                                        </div>
                                    </Transition.Child>

                                </Dialog.Panel>
                            </Transition.Child>
                        </div>
                    </Dialog>
                </Transition.Root>

                <Sidebar navigation={navigation} />

                <div className="xl:pl-72">
                    <main className="lg:pr-96">
                        <header className="flex items-center justify-between border-b border-white/5 px-4 py-4 sm:px-6 sm:py-6 lg:px-8">
                            <h1 className="text-base font-semibold leading-7 text-black">Applications</h1>
                            <SortDropdown sortOptions={sortOptions} />

                        </header>

                        <Applications apps={applications} />
                    </main>
                </div>
            </div>
        </>
    )
}


export default UserHome;